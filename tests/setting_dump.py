import json
from configparser import ConfigParser
from io import StringIO

from src import MqttSetting, AppSetting, SerialSetting


def dump():
    _parser = ConfigParser()
    _parser[SerialSetting.KEY] = SerialSetting().__dict__
    _parser[MqttSetting.KEY] = MqttSetting().__dict__

    with StringIO() as ss:
        _parser.write(ss)
        ss.seek(0)
        return ss.read()


if __name__ == '__main__':
    setting = dump()
    print(setting)
    parser = ConfigParser()
    parser.read_string(setting)
    app_setting = AppSetting()._reload(parser)
    print(type(app_setting.mqtt))
    print(type(app_setting.serial))
    print(json.dumps(app_setting.mqtt.__dict__))
