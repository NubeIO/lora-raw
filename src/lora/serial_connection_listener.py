import logging
import time

from serial import Serial

from src.ini_config import settings__enable_mqtt, mqtt__publish_value, mqtt__attempt_reconnect_secs
from src.lora.clean_payload import CleanPayload
from src.lora.decoder import LoRaV1DropletDecoder
from src.lora.droplet_registry import DropletsRegistry
from src.lora.run_decoder import run_decoder
from src.models.model_sensor import SensorModel
from src.models.model_sensor_store import SensorStoreModel
from src.models.model_serial import SerialDriverModel
from src.mqtt_client import MqttClient

logger = logging.getLogger(__name__)


class SerialConnectionListener:
    __instance = None

    def __init__(self):
        if SerialConnectionListener.__instance:
            raise Exception("SerialConnectionListener class is a singleton class!")
        else:
            self.__connection = None
            SerialConnectionListener.__instance = self

    @staticmethod
    def get_instance():
        if SerialConnectionListener.__instance is None:
            SerialConnectionListener()
        return SerialConnectionListener.__instance

    def status(self):
        return self.__connection is not None

    def start(self):
        try:
            serial_driver = SerialDriverModel.create_default_server_if_does_not_exist()
            self.__connect(serial_driver)
            if settings__enable_mqtt and mqtt__publish_value:
                while not MqttClient.get_instance().status():
                    logger.warning("MQTT is not connected, waiting for MQTT connection successful...")
                    time.sleep(mqtt__attempt_reconnect_secs)
            logger.info("MQTT is connected successfully for publishing values...")
            self.__sync_droplets_and_publish_on_mqtt()
            self.__read_and_store_value()
        except Exception as e:
            logging.error(f'Error: {str(e)}')

    def restart(self, old_serial_driver, new_serial_driver):
        """
        It tries to establish connection with new configuration,
        If it fails it will re-establish connection with old one,
        Even this re-establishment with old one got error, we send an error message
        """
        pass

    def __sync_droplets_and_publish_on_mqtt(self):
        for point in SensorModel.get_all():
            DropletsRegistry.get_instance().add_droplet(point.object_name, point.uuid)
            point_store = point.sensor_store
            MqttClient.publish_mqtt_value(point.object_name, {
                "pressure": point_store.pressure,
                "temp": point_store.temp,
                "humidity": point_store.humidity,
                "voltage": point_store.voltage,
                "rssi": point_store.rssi,
                "snr": point_store.snr,
            })

    def __connect(self, serial_driver: SerialDriverModel):
        self.__connection = Serial()
        self.__connection.port = serial_driver.port
        self.__connection.baudrate = serial_driver.baud_rate
        self.__connection.stopbits = serial_driver.stop_bits
        self.__connection.timeout = serial_driver.timeout
        self.__connection.parity = serial_driver.parity.name
        try:
            self.__connection.open()
            logger.info("Worked to open serial port {}!".format(serial_driver.port))
        except:
            self.__connection = None
            logger.error("Failed to open serial port {}!".format(serial_driver.port))
            import serial.tools.list_ports
            ports = serial.tools.list_ports.comports()
            print("Available serial ports:")
            for port, desc, hwid in sorted(ports):
                print("{}: {}".format(port, desc))

    def __read_and_store_value(self):
        if not self.__connection:
            logger.error("Can't read and store value with closed connection")
            return
        while True:
            try:
                line = self.__connection.readline().rstrip()
                if line != b'':
                    data = line.decode('utf-8')
                    logger.debug("pre_clean_data {}".format({"pre_clean_data": data, "data_len": len(data)}))
                    data = CleanPayload(data)
                    data = data.clean_data()
                    droplet = LoRaV1DropletDecoder(data)
                    logger.debug("after clean {}".format(
                        {"after_clean_data": data, "data_len": len(data), "check_len": droplet.check_payload_len()}))
                    payload = run_decoder(droplet, DropletsRegistry.get_instance().get_droplets())
                    logger.debug("MQTT PAYLOAD {}".format(payload))
                    if payload is not None:
                        uuid = DropletsRegistry.get_instance().get_uuid_from_droplets(droplet.decode_id())
                        SensorStoreModel.filter_by_sensor_uuid(uuid).update(payload)
                        SensorStoreModel.commit()
                        MqttClient.publish_mqtt_value(droplet.decode_id(), payload)
            except Exception as e:
                logger.error("{}".format(e))
