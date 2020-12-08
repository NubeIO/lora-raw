"""Load configuration from .ini file."""
import configparser

import os

config = configparser.ConfigParser()
if os.environ.get("data_dir") is None:
    filename = 'settings/config.ini'
else:
    filename = os.path.join(os.environ.get("data_dir"), 'config.ini')

config.read(filename)

settings__enable_mqtt = config.getboolean('settings', 'enable_mqtt', fallback=False)
settings__enable_serial_driver = config.getboolean('settings', 'enable_serial_driver', fallback=True)


serial__name = config.get('serial', 'name', fallback='lora-raw-network')
serial__port = config.get('serial', 'port', fallback='/dev/ttyUSB3')
serial__baud_rate = config.getint('serial', 'baud_rate', fallback=38400)
serial__stop_bits = config.getint('serial', 'stop_bits', fallback=1)
serial__parity = config.get('serial', 'parity', fallback='N')
serial__byte_size = config.getint('serial', 'byte_size', fallback=8)
serial__timeout = config.getint('serial', 'timeout', fallback=5)


mqtt__host = config.get('mqtt', 'host', fallback='0.0.0.0')
mqtt__port = config.getint('mqtt', 'port', fallback=1883)
mqtt__keepalive = config.getint('mqtt', 'keepalive', fallback=60)
mqtt__qos = config.getint('mqtt', 'qos', fallback=1)
mqtt__retain = config.getboolean('mqtt', 'retain', fallback=False)
mqtt__publish_value = config.getboolean('mqtt', 'publish_value', fallback=True)
mqtt__attempt_reconnect_on_unavailable = config.getboolean('mqtt', 'attempt_reconnect_on_unavailable', fallback=True)
mqtt__attempt_reconnect_secs = config.getint('mqtt', 'attempt_reconnect_secs', fallback=5)
