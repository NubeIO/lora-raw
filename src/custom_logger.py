import logging

from src.mqtt_client import MqttClient, mqtt__debug_topic, mqtt__debug


class CustomLogger(logging.Logger):
    def debug(self, msg, *args, **kwargs):
        if mqtt__debug:
            self.publish_mqtt_topic(msg, 'DEBUG', args, kwargs)
        if self.force_to_console(**kwargs):
            return super(CustomLogger, self).debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        if mqtt__debug:
            self.publish_mqtt_topic(msg, 'INFO', args, kwargs)
        if self.force_to_console(**kwargs):
            return super(CustomLogger, self).info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if mqtt__debug:
            self.publish_mqtt_topic(msg, 'WARNING', args, kwargs)
        if self.force_to_console(**kwargs):
            return super(CustomLogger, self).warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if mqtt__debug:
            self.publish_mqtt_topic(msg, 'ERROR', args, kwargs)
        if self.force_to_console(**kwargs):
            return super(CustomLogger, self).error(msg, *args, **kwargs)

    def force_to_console(self, **kwargs):
        return not kwargs.get('stacklevel') == 0

    def publish_mqtt_topic(self, msg, level, args, kwargs):
        formatted_msg = msg % args % kwargs
        payload = '{}: {}'.format(level, formatted_msg)
        MqttClient.publish_mqtt_value(mqtt__debug_topic, payload)
