#!/usr/bin/env python3

import multiprocessing
import os

import click
from gunicorn.glogging import Logger
from gunicorn.workers.ggevent import GeventWorker

from src import create_app, AppSetting, GunicornFlaskApplication

CLI_CTX_SETTINGS = dict(help_option_names=["-h", "--help"], max_content_width=120)


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


@click.command(context_settings=CLI_CTX_SETTINGS)
@click.option('-p', '--port', type=int, default=1919, show_default=True, help='Port')
@click.option('-d', '--data-dir', type=click.Path(), help='Application data dir',
              default=lambda: os.environ.get(AppSetting.DATA_DIR_ENV, AppSetting.default_data_dir))
@click.option('--prod', is_flag=True, help='Production mode')
@click.option('-s', '--setting-file', help='Rubix-Lora: setting ini file')
@click.option('-l', '--logging-conf', help='Rubix-Lora: logging config file')
@click.option('--workers', type=int, default=lambda: number_of_workers(),
              help='Gunicorn: The number of worker processes for handling requests.')
@click.option('-c', '--gunicorn-config', help='Gunicorn: config file(gunicorn.conf.py)')
@click.option('--log-level', type=click.Choice(['FATAL', 'ERROR', 'WARN', 'INFO', 'DEBUG'], case_sensitive=False),
              show_default=True, help='Logging level')
def cli(port, data_dir, prod, workers, setting_file, logging_conf, gunicorn_config, log_level):
    setting = AppSetting(data_dir=data_dir, prod=prod).reload(setting_file, logging_conf)
    options = {
        'bind': '%s:%s' % ('0.0.0.0', port),
        'workers': workers if prod else 1,
        'worker_class': GeventWorker.__module__ + '.' + GeventWorker.__qualname__,
        'logger_class': Logger.__module__ + '.' + Logger.__name__,
        'log_level': ('INFO' if prod else 'DEBUG' if log_level is None else log_level).lower(),
        'preload_app': True,
        'config': gunicorn_config
    }
    GunicornFlaskApplication(create_app(setting), options).run()


if __name__ == '__main__':
    cli()
