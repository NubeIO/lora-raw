from src import MqttSetting
from src.mqtt import MqttClient

if __name__ == '__main__':
    MqttClient().start(MqttSetting(), loop_forever=False)
    print(MqttClient().make_topic((MqttClient().config.topic,) + ("id", "name")))
