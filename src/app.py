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
from functools import partial

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()


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

    def setup(self):
        with self.app_context():
            gunicorn_logger = logging.getLogger('gunicorn.error')
            self.logger.handlers = gunicorn_logger.handlers
            self.logger.setLevel(gunicorn_logger.level)
            self.logger.info(self.config['SQLALCHEMY_DATABASE_URI'])
            db.create_all()
            from src.background import Background
            Background.run()

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, _):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    def register_router(_app) -> Flask:
        from src.routes import bp_lora, bp_system
        _app.register_blueprint(bp_system)
        _app.register_blueprint(bp_lora)
        return _app

    app.setup = partial(setup, app)
    return register_router(app)
