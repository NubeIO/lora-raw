import logging.config
import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine.base import Engine

from src.custom_logger import CustomLogger

logging.setLoggerClass(CustomLogger)

if os.environ.get("data_dir") is None:
    logging_file = 'logging/logging.conf'
else:
    logging_file = os.path.join(os.environ.get("data_dir"), 'logging.conf')

try:
    logging.config.fileConfig(logging_file)
except Exception as e:
    raise Exception(
        f'Failed to load logging config file {logging_file}. Assure the example config is cloned as logging.conf')

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

if os.environ.get("data_dir") is None:
    url = 'sqlite:///data.db?timeout=60&check_same_thread=false'
else:
    url = "sqlite:///{}/data.db?timeout=60&check_same_thread=false".format(os.environ.get("data_dir"))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', url)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False  # for print the sql query

db = SQLAlchemy(app)

from src import routes  # importing for creating all the schema on un-existing case

db.create_all()

with app.app_context():
    if os.environ.get("WERKZEUG_RUN_MAIN") or os.environ.get('SERVER_SOFTWARE'):
        from src.background import Background

        Background.run()
