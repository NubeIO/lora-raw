import logging

from rubix_mqtt.mqtt import MqttClientBase

from src import MqttSetting
from src.utils import Singleton

logger = logging.getLogger(__name__)


class MqttClient(MqttClientBase, metaclass=Singleton):

    @property
    def config(self) -> MqttSetting:
        return super().config

    def publish_mqtt_value(self, topic, payload):
        if not self.status():
            logger.error(f"MQTT client {self.to_string()} is not connected...")
            return
        logger.debug(
            "MQTT_PUBLISH: 'topic': {}, 'payload': {}, 'retain': {}".format(topic, payload, self.config.retain))
        self.client.publish(topic, str(payload), qos=self.config.qos, retain=self.config.retain)

    def publish_raw(self, payload):
        self.publish_mqtt_value(self.config.raw_topic, payload)

    def publish_debug(self, payload):
        self.publish_mqtt_value(self.config.debug_topic, payload)

    def get_topic(self, name):
        return "{}/{}".format(self.config.topic, name)
