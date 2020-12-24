from logging import Logger

import paho.mqtt.client as mqtt_client
import time
from flask import current_app
from werkzeug.local import LocalProxy

from src.app import MqttSetting
from src.utils import Singleton

logger = LocalProxy(lambda: current_app.logger) or Logger(__name__)


class MqttClient(metaclass=Singleton):

    def __init__(self):
        self.__config = None
        self.__client = None

    @property
    def config(self) -> MqttSetting:
        return self.__config

    def status(self) -> bool:
        return self.__client.is_connected() if self.config and self.config.enabled and self.__client else False

    def start(self, config: MqttSetting):
        self.__config = config
        self.__client = mqtt_client.Client(self.config.name)
        self.__client.on_connect = self.__on_connect
        if self.config.attempt_reconnect_on_unavailable:
            while True:
                try:
                    self.__client.connect(config.host, config.port, config.keepalive)
                    break
                except ConnectionRefusedError:
                    logger.error('MQTT connection failure: ConnectionRefusedError. \
                                    Attempting reconnect in {} seconds'.format(config.attempt_reconnect_secs))
                    time.sleep(config.attempt_reconnect_secs)
        else:
            try:
                self.__client.connect(config.host, config.port, config.keepalive)
            except Exception as e:
                self.__client = None
                logger.error(str(e))
                return
        self.__client.loop_forever()

    def get_topic(self, name):
        return "{}/{}".format(self.config.topic, name)

    def publish_mqtt_value(self, topic, payload):
        if not self.status():
            logger.error("MQTT is not connected...", stacklevel=0)
            return
        logger.debug(
            "MQTT_PUBLISH: 'topic': {}, 'payload': {}, 'retain': {}".format(topic, payload, self.config.retain),
            stacklevel=0)
        self.__client.publish(topic, str(payload), qos=self.config.qos, retain=self.config.retain)

    def publish_log(self, payload):
        self.publish_mqtt_value(self.config.debug_topic, payload)

    def __on_connect(self, client, userdata, flags, reason_code, properties=None):
        if reason_code > 0:
            reasons = {
                1: 'Connection refused - incorrect protocol version',
                2: 'Connection refused - invalid client identifier',
                3: 'Connection refused - serial_driver unavailable',
                4: 'Connection refused - bad username or password',
                5: 'Connection refused - not authorised'
            }
            reason = reasons.get(reason_code, 'unknown')
            self.__client = None
            raise Exception("MQTT Connection Failure: {}".format(reason))