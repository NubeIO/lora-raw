import json
import os
from abc import ABC

from flask import Flask


class BaseSetting(ABC):

    def reload(self, setting: dict):
        if setting is not None:
            self.__dict__ = {k: setting.get(k, v) for k, v in self.__dict__.items()}
        return self

    def serialize(self, pretty=True) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, indent=2 if pretty else None)

    def to_dict(self):
        return json.loads(self.serialize(pretty=False))


class SerialSetting(BaseSetting):
    KEY = 'serial'

    def __init__(self):
        self.enabled: bool = True
        self.name: str = 'lora-raw-network'
        self.port: str = '/dev/ttyUSB0'
        self.baud_rate = 9600
        self.stop_bits = 1
        self.parity: str = 'N'
        self.byte_size = 8
        self.timeout = 5
        self.firmware_version = 'v1'
        self.encryption_key = ''


class MqttSetting(BaseSetting):
    KEY = 'mqtt'

    def __init__(self):
        self.enabled = True
        self.name = 'lora-raw-mqtt'
        self.host = '0.0.0.0'
        self.port = 1883
        self.keepalive = 60
        self.qos = 1
        self.retain = False
        self.attempt_reconnect_on_unavailable = True
        self.attempt_reconnect_secs = 5
        self.topic = 'lora_raw'
        self.debug = True
        self.debug_topic = 'debug_lora_raw'


class AppSetting:
    DATA_DIR_ENV = 'RUBIX_LORA_DATA'
    SETTING_FILE_ENV = 'RUBIX_LORA_SETTING'
    LOGGING_CONF_ENV = 'RUBIX_LORA_LOG_CONF'
    KEY: str = 'APP_SETTING'
    default_data_dir: str = 'out'
    default_setting_file: str = 'config.json'
    default_logging_conf: str = 'logging.conf'

    def __init__(self, **kwargs):
        self.__data_dir = self.__compute_dir(kwargs.get('data_dir'), AppSetting.default_data_dir)
        self.__prod = kwargs.get('prod') or False
        self.__mqtt_setting = MqttSetting()
        self.__serial_setting = SerialSetting()

    @property
    def data_dir(self):
        return self.__data_dir

    @property
    def prod(self) -> bool:
        return self.__prod

    @property
    def mqtt(self) -> MqttSetting:
        return self.__mqtt_setting

    @property
    def serial(self) -> SerialSetting:
        return self.__serial_setting

    def serialize(self, pretty=True) -> str:
        m = {MqttSetting.KEY: self.mqtt, SerialSetting.KEY: self.serial, 'prod': self.prod, 'data_dir': self.data_dir}
        return json.dumps(m, default=lambda o: o.to_dict() if isinstance(o, BaseSetting) else o.__dict__,
                          indent=2 if pretty else None)

    def reload(self, setting_file: str, logging_file: str, is_json_str=False):
        data = self.__read_file(setting_file, self.__data_dir, is_json_str)
        self.__mqtt_setting = self.__mqtt_setting.reload(data.get(MqttSetting.KEY, None))
        self.__serial_setting = self.__serial_setting.reload(data.get(SerialSetting.KEY, None))
        return self

    def init_app(self, app: Flask):
        app.config[AppSetting.KEY] = self
        return self

    @staticmethod
    def __compute_dir(_dir: str, _def: str, mode=0o744) -> str:
        d = os.path.join(os.getcwd(), _def) if _dir is None or _dir.strip() == '' else _dir
        d = d if os.path.isabs(d) else os.path.join(os.getcwd(), d)
        os.makedirs(d, mode, True)
        return d

    @staticmethod
    def __read_file(setting_file: str, _dir: str, is_json_str=False):
        if is_json_str:
            return json.loads(setting_file)
        if setting_file is None or setting_file.strip() == '':
            return {}
        s = setting_file if os.path.isabs(setting_file) else os.path.join(_dir, setting_file)
        if not os.path.isfile(s) or not os.path.exists(s):
            return {}
        with open(s) as json_file:
            return json.load(json_file)
