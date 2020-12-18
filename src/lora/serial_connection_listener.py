import logging
import time
from threading import Thread

import serial.tools.list_ports
from serial import Serial

from src.ini_config import settings__enable_mqtt, mqtt__attempt_reconnect_secs
from src.lora.decoders.decoder import DecoderFactory
from src.lora.decoders.decoder_base import DecoderBase
from src.lora.device_registry import DeviceRegistry
from src.models.model_sensor import SensorModel
from src.models.model_sensor_store import SensorStoreModel
from src.models.model_serial import SerialDriverModel
from src.mqtt_client import MqttClient

logger = logging.getLogger(__name__)


class SerialConnectionListener:
    __instance = None
    __thread = None

    def __init__(self):
        if SerialConnectionListener.__instance:
            raise Exception("SerialConnectionListener class is a singleton class!")
        else:
            self.__connection = None
            self.__serial_driver = None
            self.__new_serial_driver = None
            SerialConnectionListener.__instance = self

    @staticmethod
    def get_instance():
        if SerialConnectionListener.__instance is None:
            SerialConnectionListener()
        return SerialConnectionListener.__instance

    def status(self):
        return self.__connection is not None

    def start(self):
        serial_driver = SerialDriverModel.create_default_server_if_does_not_exist()
        self.__serial_driver = serial_driver
        self.__start_thread()

    def restart(self, new_serial_driver):
        self.__new_serial_driver = new_serial_driver
        logger.info("Restarting the serial driver...")

    def __start_thread(self):
        SerialConnectionListener.__thread = Thread(target=self.__start, daemon=True)
        SerialConnectionListener.__thread.start()

    def __start(self):
        try:
            self.__connect()
            if settings__enable_mqtt:
                time.sleep(1)  # time for mqtt client to connect
                while not MqttClient.get_instance().status():
                    logger.warning("MQTT not connected. Waiting for MQTT connection successful...")
                    time.sleep(mqtt__attempt_reconnect_secs)
                logger.info("MQTT client connected. Resuming...")
            self.__sync_devices()
            self.__read_and_store_value()
        except Exception as e:
            self.__connection = None
            logging.error("Error: {}".format(str(e)))

    def __sync_devices(self):
        for point in SensorModel.get_all():
            DeviceRegistry.get_instance().add_device(point.device_id, point.uuid)
            point_store = point.sensor_store
            if settings__enable_mqtt:
                # TODO: move this and publish other sensor values
                MqttClient.publish_mqtt_value(point.name, {
                    "pressure": point_store.pressure,
                    "temp": point_store.temp,
                    "humidity": point_store.humidity,
                    "voltage": point_store.voltage,
                    "rssi": point_store.rssi,
                    "snr": point_store.snr,
                })

    def __connect(self):
        self.__connection = Serial()
        self.__connection.port = self.__serial_driver.port
        self.__connection.baudrate = self.__serial_driver.baud_rate
        self.__connection.stopbits = self.__serial_driver.stop_bits
        self.__connection.timeout = self.__serial_driver.timeout
        self.__connection.parity = self.__serial_driver.parity.name
        try:
            self.__connection.open()
            logger.info("Serial port {} opened!".format(self.__serial_driver.port))
            return
        except:
            self.__connection = None
            logger.error("Failed to open serial port {}".format(self.__serial_driver.port))
            ports = serial.tools.list_ports.comports()
            logger.info("Available serial ports are:")
            i = 0
            for port, desc, _ in sorted(ports):
                i += 1
                logger.info("{}. {}: {}".format(i, port, desc))

    def __read_and_store_value(self):
        while True:
            if self.__serial_driver != self.__new_serial_driver and self.__new_serial_driver:
                # when restart occurs
                self.__serial_driver = self.__new_serial_driver
                self.__start()
            try:
                if not self.__connection:
                    raise Exception('Connection not established')
                data = self.__connection.readline().strip().decode('utf-8')
                self.__store_value(data)
            except Exception as e:
                logger.error(str(e))
                if self.__connection:
                    self.__connection.close()
                    self.__connection = None
                time.sleep(5)
                # retry when reading got failed (unplugging device, device port un-match etc.)
                self.__start()

    def __store_value(self, data):
        if data and DecoderBase.check_payload_len(data):
            logger.debug("   payload: {} length: {}".format(data, len(data)))
            decoder = DecoderFactory.get_decoder(data)
            if decoder is None:
                logger.warning('No decoder found... Continuing')
            else:
                sensor_id = decoder.decode_id()
                if sensor_id in DeviceRegistry.get_instance().get_devices():
                    payload = decoder.decode()
                    logger.debug('    Sensor payload: {}'.format(payload))
                    if payload is not None:
                        uuid = DeviceRegistry.get_instance().get_uuid_from_devices(sensor_id)
                        SensorStoreModel.filter_by_sensor_uuid(uuid).update(payload)
                        SensorStoreModel.commit()
                        MqttClient.publish_mqtt_value(sensor_id, payload)
                else:
                    logger.warning('      Sensor not in registry: {}'.format(sensor_id))
        elif data:
            logger.debug("Raw serial: {}".format(data))
