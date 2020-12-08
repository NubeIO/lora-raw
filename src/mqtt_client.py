import logging
import time

import paho.mqtt.client as mqtt_client

from src.ini_config import *

MQTT_CLIENT_NAME = 'lora-raw-mqtt'

logger = logging.getLogger(__name__)


class MqttClient:
    __instance = None
    __client = None

    def __init__(self):
        if MqttClient.__instance:
            raise Exception("MqttConnection class is a singleton class!")
        else:
            MqttClient.__instance = self

    @staticmethod
    def get_instance():
        if MqttClient.__instance is None:
            MqttClient()
        return MqttClient.__instance

    def status(self) -> bool:
        if not MqttClient.__client:
            return False
        else:
            return MqttClient.__client.is_connected()

    def start(self):
        MqttClient.__client = mqtt_client.Client(MQTT_CLIENT_NAME)
        MqttClient.__client.on_connect = MqttClient.__on_connect
        if mqtt__attempt_reconnect_on_unavailable:
            while True:
                try:
                    MqttClient.__client.connect(mqtt__host, mqtt__port, mqtt__keepalive)
                    break
                except ConnectionRefusedError:
                    logger.error(
                        'MQTT connection failure: ConnectionRefusedError. Attempting reconnect in {} seconds'.format(
                            mqtt__attempt_reconnect_secs))
                    time.sleep(mqtt__attempt_reconnect_secs)
        else:
            try:
                MqttClient.__client.connect(mqtt__host, mqtt__port, mqtt__keepalive)
            except Exception as e:
                MqttClient.__client = None
                logger.error(str(e))
                return
        MqttClient.__client.loop_forever()

    @staticmethod
    def publish_mqtt_value(object_name, payload: dict):
        topic = "lora_raw/{}".format(object_name)
        retain = mqtt__retain
        if not MqttClient.get_instance().status():
            logger.error("MQTT is not connected...")
            logging.error(
                "Failed MQTT_PUBLISH: 'topic': {}, 'payload': {}, 'retain': {}".format(topic, payload, retain))
            return
        logging.debug("MQTT_PUBLISH: 'topic': {}, 'payload': {}, 'retain': {}".format(topic, payload, retain))
        MqttClient.__client.publish(topic, str(payload), qos=mqtt__qos, retain=retain)

    @staticmethod
    def __on_connect(client, userdata, flags, reason_code, properties=None):
        if reason_code > 0:
            reasons = {
                1: 'Connection refused - incorrect protocol version',
                2: 'Connection refused - invalid client identifier',
                3: 'Connection refused - serial_driver unavailable',
                4: 'Connection refused - bad username or password',
                5: 'Connection refused - not authorised'
            }
            reason = reasons.get(reason_code, 'unknown')
            MqttClient.__client = None
            raise Exception(f'MQTT Connection Failure: {reason}')
