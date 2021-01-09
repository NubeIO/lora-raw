import logging

from src.mqtt import MqttClient


class CustomLogger(logging.Logger):
    def debug(self, msg, *args, **kwargs):
        if MqttClient().config and MqttClient().config.publish_debug:
            self.publish_mqtt_topic(msg, 'DEBUG', *args, **kwargs)
        return super(CustomLogger, self).debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        if MqttClient().config and MqttClient().config.publish_debug:
            self.publish_mqtt_topic(msg, 'INFO', *args, **kwargs)
        return super(CustomLogger, self).info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if MqttClient().config and MqttClient().config.publish_debug:
            self.publish_mqtt_topic(msg, 'WARNING', *args, **kwargs)
        return super(CustomLogger, self).warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if MqttClient().config and MqttClient().config.publish_debug:
            self.publish_mqtt_topic(msg, 'ERROR', *args, **kwargs)
        return super(CustomLogger, self).error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        if MqttClient().config and MqttClient().config.publish_debug:
            self.publish_mqtt_topic(msg, 'CRITICAL', *args, **kwargs)
        return super(CustomLogger, self).critical(msg, *args, **kwargs)

    def publish_mqtt_topic(self, msg, level, *args, **kwargs):
        formatted_msg = msg % args % kwargs
        payload = '{}: {}'.format(level, formatted_msg)
        MqttClient().publish_debug(payload)
