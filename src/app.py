# from src.custom_logger import CustomLogger
#
# logging.setLoggerClass(CustomLogger)
#
# if os.environ.get("data_dir") is None:
#     logging_file = 'logging/logging.conf'
# else:
#     logging_file = os.path.join(os.environ.get("data_dir"), 'logging.conf')
#
# try:
#     logging.config.fileConfig(logging_file)
# except Exception as e:
#     raise Exception(
#         f'Failed to load logging config file {logging_file}. Assure the example config is cloned as logging.conf')
import logging
import os
from configparser import ConfigParser

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()


class MqttSetting:

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

    def reload(self, setting: dict):
        if setting is not None:
            self.__dict__ = {k: setting[k] or v for k, v in self.__dict__.items()}
        return self


class SerialSetting:

    def __init__(self):
        self.enabled: bool = True
        self.name: str = 'lora-raw-network'
        self.port: str = '/dev/ttyUSB0'
        self.baud_rate = 9600
        self.stop_bits = 1
        self.parity: str = 'N'
        self.byte_size = 8
        self.timeout = 5

    def reload(self, setting: dict):
        if setting is not None:
            self.__dict__ = {k: setting[k] or v for k, v in self.__dict__.items()}
        return self


class AppSetting:
    default_data_dir: str = 'out'
    KEY: str = 'APP_SETTING'

    def __init__(self, **kwargs):
        self._data_dir = self.__compute_dir(kwargs['data_dir'], AppSetting.default_data_dir)
        self._prod = kwargs['prod'] or False
        self._mqtt_setting = MqttSetting()
        self._serial_setting = SerialSetting()

    @property
    def data_dir(self):
        return self._data_dir

    @property
    def prod(self) -> bool:
        return self._prod

    @property
    def mqtt(self) -> MqttSetting:
        return self._mqtt_setting

    @property
    def serial(self) -> SerialSetting:
        return self._serial_setting

    def reload(self, setting_file: str, logging_file: str):
        parser = self.__read_file(setting_file, self._data_dir)
        self._mqtt_setting = self._mqtt_setting.reload(self.__load_setting('mqtt', parser))
        self._serial_setting = self._serial_setting.reload(self.__load_setting('serial', parser))
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
    def __read_file(setting_file: str, _dir: str):
        if setting_file is None or setting_file.strip() == '':
            return None
        s = setting_file if os.path.isabs(setting_file) else os.path.join(_dir, setting_file)
        if not os.path.isfile(s) or not os.path.exists(s):
            return None
        parser = ConfigParser()
        parser.read(setting_file)
        return parser

    @staticmethod
    def __load_setting(section: str, parser: ConfigParser):
        if parser is None:
            return None
        return dict(parser.items(section)) if parser.has_section(section) else None


def create_app(app_setting) -> Flask:
    os.environ.setdefault('FLASK_ENV', 'production' if app_setting.prod else 'development')
    app = Flask(__name__)
    cors = CORS()
    app_setting = app_setting.init_app(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/data.db?timeout=60'.format(app_setting.data_dir)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    cors.init_app(app)
    db.init_app(app)

    # with app.app_context():
    #     if os.environ.get("WERKZEUG_RUN_MAIN") or os.environ.get('SERVER_SOFTWARE'):
    #         from src.background import Background
    #         Background.run()

    @app.before_first_request
    def setup():
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
        app.logger.info(app.config['SQLALCHEMY_DATABASE_URI'])
        db.create_all()

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, _):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    def register_router(_app) -> Flask:
        from src.routes import bp_lora
        from src.routes import bp_system
        _app.register_blueprint(bp_system)
        _app.register_blueprint(bp_lora)
        return _app

    return register_router(app)
