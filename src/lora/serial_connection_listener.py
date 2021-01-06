import time
from logging import Logger

import serial.tools.list_ports
from serial import Serial

from src import SerialSetting
from src.lora import DeviceRegistry
from src.lora.decoders.decoder import DecoderFactory
from src.lora.decoders.decoder_base import DecoderBase
from src.models.model_sensor import SensorModel
from src.models.model_sensor_store import SensorStoreModel
from src.models.model_serial import SerialDriverModel
from src.mqtt import MqttClient
from src.utils import Singleton


class SerialConnectionListener(metaclass=Singleton):
    def __init__(self):
        self.__config = None
        self.__connection = None
        self.__serial_driver = None
        self.__new_serial_driver = None
        self.logger = None

    def status(self):
        return self.__connection is not None

    def start(self, config: SerialSetting, logger: Logger):
        self.logger = logger or Logger(__name__)
        self.__config = config
        self.__serial_driver = SerialDriverModel.create_default_server_if_does_not_exist(self.__config)
        self.__start()

    def restart(self, new_serial_driver):
        self.__new_serial_driver = new_serial_driver
        self.logger.info("Restarting the serial driver...")

    def __start(self):
        try:
            self.__connect()
            mqttc = MqttClient()
            if mqttc.config.enabled:
                time.sleep(1)  # time for mqtt client to connect
                while not mqttc.status():
                    self.logger.warning("MQTT not connected. Waiting for MQTT connection successful...")
                    time.sleep(mqttc.config.attempt_reconnect_secs)
            self.__sync_devices()
            self.__read_and_store_value()
        except Exception as e:
            self.__connection = None
            self.logger.error("Error: {}".format(str(e)))

    def __sync_devices(self):
        mqttc = MqttClient()
        for point in SensorModel.get_all():
            DeviceRegistry().add_device(point.device_id, point.uuid, point.name)
            point_store = point.sensor_store
            if mqttc.config.enabled:
                topic = mqttc.get_topic(point.name)
                mqttc.publish_mqtt_value(topic, point_store.get_value())

    def __connect(self):
        self.__connection = Serial()
        self.__connection.port = self.__serial_driver.port
        self.__connection.baudrate = self.__serial_driver.baud_rate
        self.__connection.stopbits = self.__serial_driver.stop_bits
        self.__connection.timeout = self.__serial_driver.timeout
        self.__connection.parity = self.__serial_driver.parity.name
        try:
            self.__connection.open()
            self.logger.info("Serial port {} opened!".format(self.__serial_driver.port))
            return
        except:
            self.__connection = None
            self.logger.error("Failed to open serial port {}".format(self.__serial_driver.port))
            ports = serial.tools.list_ports.comports()
            self.logger.info("Available serial ports are:")
            i = 0
            for port, desc, _ in sorted(ports):
                i += 1
                self.logger.info("{}. {}: {}".format(i, port, desc))

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
                self.logger.error(str(e))
                if self.__connection:
                    self.__connection.close()
                    self.__connection = None
                time.sleep(5)
                # retry when reading got failed (unplugging device, device port un-match etc.)
                self.__start()

    def __store_value(self, data):
        if data and DecoderBase.check_payload_len(data):
            self.logger.debug("   payload: {} length: {}".format(data, len(data)))
            decoder = DecoderFactory.get_decoder(data)
            if decoder is None:
                self.logger.warning('No decoder found... Continuing')
            else:
                device_id = decoder.decode_id()
                devices = DeviceRegistry().get_devices()
                if device_id in devices:
                    payload = decoder.decode()
                    self.logger.debug('    Sensor payload: {}'.format(payload))
                    if payload is not None:
                        (uuid, name) = DeviceRegistry().get_device(device_id)
                        SensorStoreModel.filter_by_sensor_uuid(uuid).update(payload)
                        SensorStoreModel.commit()
                        mqttc = MqttClient()
                        mqttc.publish_mqtt_value(mqttc.get_topic(name), payload)
                else:
                    self.logger.warning('      Sensor not in registry: {}'.format(device_id))
        elif data:
            self.logger.debug("Raw serial: {}".format(data))
