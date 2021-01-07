from logging import Logger
from threading import Thread

from flask import current_app
from werkzeug.local import LocalProxy

from .setting import AppSetting


class FlaskThread(Thread):
    """
    To make every new thread behinds Flask app context.
    Maybe using another lightweight solution but richer: APScheduler <https://github.com/agronholm/apscheduler>
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = current_app._get_current_object()

    def run(self):
        with self.app.app_context():
            super().run()


# TODO: Should refactor to stop when receive exit code
class Background:
    @staticmethod
    def run():
        from src.lora import SerialConnectionListener
        from src.mqtt import MqttClient
        setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        logger = LocalProxy(lambda: current_app.logger) or Logger(__name__)
        logger.info("Running Background Task...")
        if setting.mqtt.enabled:
            FlaskThread(target=MqttClient().start, daemon=True,
                        kwargs={'config': setting.mqtt, 'logger': logger}).start()

        if setting.serial.enabled:
            SerialConnectionListener().start(setting.serial, logger)
