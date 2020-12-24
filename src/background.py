from logging import Logger
from threading import Thread

from flask import current_app
from werkzeug.local import LocalProxy

from src.app import AppSetting
from src.lora.serial_connection_listener import SerialConnectionListener
from src.mqtt import MqttClient

logger = LocalProxy(lambda: current_app.logger) or Logger(__name__)


# TODO: Should refactor to stop when receive exit code
class Background:
    @staticmethod
    def run():
        setting: AppSetting = current_app.config[AppSetting.KEY]
        logger.info("Running Background Task...")
        if setting.mqtt.enabled:
            mqtt_thread = Thread(target=MqttClient().start, daemon=True, kwargs={'config': setting.mqtt})
            mqtt_thread.start()

        if setting.serial.enabled:
            SerialConnectionListener().start(setting.serial)
