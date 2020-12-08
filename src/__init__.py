import logging.config
import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

logging.config.fileConfig('logging/logging.conf')

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

if os.environ.get("data_dir") is None:
    url = 'sqlite:///data.db?timeout=60&check_same_thread=false'
else:
    url = f'sqlite:///{os.environ.get("data_dir")}/data.db?timeout=60&check_same_thread=false'

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
