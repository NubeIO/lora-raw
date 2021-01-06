from abc import ABC

from gunicorn.app.base import BaseApplication
from gunicorn.arbiter import Arbiter
from gunicorn.glogging import Logger
from gunicorn.workers.ggevent import GeventWorker

from .app import create_app, db
from .setting import AppSetting


def init_gunicorn_option(_options=None):
    from gevent import monkey as curious_george
    curious_george.patch_all()
    # curious_george.patch_all(thread=False)
    options = _options or {}
    options.update({'worker_class': GeventWorker.__module__ + '.' + GeventWorker.__qualname__,
                    'logger_class': Logger.__module__ + '.' + Logger.__name__,
                    'when_ready': when_ready,
                    'on_exit': on_exit})
    return options


def on_exit(server: Arbiter):
    server.log.info('Server is stopped')


def when_ready(server: Arbiter):
    server.log.info("Server is ready. Spawning workers...")
    # server.app.application.setup()


class GunicornFlaskApplication(BaseApplication, ABC):

    def __init__(self, _app_setting: AppSetting, _options=None):
        self._options = init_gunicorn_option(_options)
        super(GunicornFlaskApplication, self).__init__()
        self._app_setting = _app_setting
        self.application = None

    def load_config(self):
        config = {key: value for key, value in self._options.items() if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        self.application = create_app(self._app_setting)
        return self.application

    def wsgi(self):
        output = super(GunicornFlaskApplication, self).wsgi()
        with self.application.app_context():
            db.create_all()
            from src.background import Background
            Background.run()
        return output
