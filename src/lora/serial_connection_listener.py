import json
import logging
import time

import serial.tools.list_ports
from serial import Serial

from src import SerialSetting
from src.lora import DeviceRegistry
from src.lora.decoders.decoder import DecoderFactory
from src.lora.decoders.decoder_base import DecoderBase
from src.models.model_device import DeviceModel
from src.models.model_network import NetworkModel
from src.models.model_point import PointModel
from src.mqtt import MqttClient
from src.utils import Singleton

logger = logging.getLogger(__name__)


class SerialConnectionListener(metaclass=Singleton):
    __thread = None

    def __init__(self):
        self.__config = None
        self.__connection = None
        self.__serial_driver = None
        self.__new_serial_driver = None
        self.__temp_mqttc: MqttClient = MqttClient()

    def status(self):
        return self.__connection is not None

    def start(self, config: SerialSetting):
        self.__config = config
        self.__start()

    def restart(self, new_serial_driver):
        self.__new_serial_driver = new_serial_driver
        logger.info("Restarting the serial driver...")

    def __check_and_set_restart(self) -> bool:
        if self.__new_serial_driver and self.__serial_driver != self.__new_serial_driver:
            self.__serial_driver = self.__new_serial_driver
            self.__new_serial_driver = None
            return True
        return False

    def __start(self):
        self.__register_devices()
        self.__serial_driver = NetworkModel.create_network(self.__config)
        while True:
            self.__check_and_set_restart()
            if not self.__connect_serial():
                time.sleep(5)
                continue

            try:
                if self.__temp_mqttc.config.enabled:
                    time.sleep(1)  # time for mqtt client to connect
                    while not self.__temp_mqttc.status():
                        logger.warning("MQTT not connected. Waiting for MQTT connection successful...")
                        time.sleep(self.__temp_mqttc.config.attempt_reconnect_secs)
                    logger.info("MQTT client connected. Resuming...")
            except Exception as e:
                self.__connection = None
                logger.error("Error: {}".format(str(e)))
                continue

            self.__read_serial_loop()

    def __register_devices(self):
        for device in DeviceModel.find_all():
            DeviceRegistry().add_device(device.device_id, device.uuid)

    def __connect_serial(self) -> bool:
        self.__connection = Serial()
        self.__connection.port = self.__serial_driver.port
        self.__connection.baudrate = self.__serial_driver.baud_rate
        self.__connection.stopbits = self.__serial_driver.stop_bits
        self.__connection.timeout = self.__serial_driver.timeout
        self.__connection.parity = self.__serial_driver.parity.name
        try:
            self.__connection.open()
        except:
            self.__connection = None
            logger.error("Failed to open serial port {}".format(self.__serial_driver.port))
            ports = serial.tools.list_ports.comports()
            logger.info("    Available serial ports are:")
            i = 0
            for port, desc, _ in sorted(ports):
                i += 1
                logger.info("        {}. {}".format(i, port))
            return False

        logger.info("Serial port {} opened!".format(self.__serial_driver.port))
        return True

    def __read_serial_loop(self):
        while True:
            if self.__check_and_set_restart():
                break
            if not self.__connection:
                logger.error('Connection not established')

            try:
                data = self.__connection.readline().strip().decode('utf-8')
            except Exception as e:
                # retry when reading got failed (unplugging device, device port un-match etc.)
                logger.error(str(e))
                time.sleep(5)
                break

            self.__decode_device(data)

        if self.__connection:
            self.__connection.close()
            self.__connection = None

    def __decode_device(self, data: str):
        if data and MqttClient().config and MqttClient().config.publish_raw:
            MqttClient().publish_raw(data)
        if data and DecoderBase.check_payload_len(data):
            logger.debug("payload: {} length: {}".format(data, len(data)))
            device_id = DecoderFactory.get_id(data)

            if DeviceRegistry().get_device(device_id) is None:
                logger.warning('Sensor not in registry: {}'.format(device_id))
                return

            device = DeviceModel.find_by_id(device_id)
            decoder = DecoderFactory.get_decoder(data, device.device_model)
            if decoder is None:
                logger.warning(f'No decoder found for device model {device.device_model}... Continuing')

            payload = decoder.decode()
            logger.debug('Sensor payload: {}'.format(payload))
            if payload is not None:
                points = device.points
                point: PointModel
                for key in payload:
                    for point in points:
                        if key == point.device_point_name:
                            point_store = point.point_store
                            point_store.value_original = payload[key]
                            point.update_point_value(point.point_store)
                self.__temp_mqttc.publish_value(self.__temp_mqttc.make_topic((device.device_id, device.name)), payload)
        elif data:
            logger.debug("Raw serial: {}".format(data))
