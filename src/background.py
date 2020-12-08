import logging
from threading import Thread

from src.lora.serial_connection_listener import SerialConnectionListener
from src.mqtt_client import MqttClient, settings__enable_mqtt, settings__enable_serial_driver

logger = logging.getLogger(__name__)


class Background:
    @staticmethod
    def run():
        logger.info("Running Background Task...")
        if settings__enable_mqtt:
            mqtt_thread = Thread(target=MqttClient.get_instance().start, daemon=True)
            mqtt_thread.start()

        if settings__enable_serial_driver:
            SerialConnectionListener.get_instance().start()
