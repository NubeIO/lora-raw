from src import AppSetting, SerialSetting

if __name__ == '__main__':
    setting = '''
    {
      "mqtt": {
        "enabled": true,
        "name": "lora-raw-mqtt",
        "host": "0.0.0.0",
        "port": 1883,
        "keepalive": 60,
        "qos": 1,
        "retain": false,
        "attempt_reconnect_on_unavailable": true,
        "attempt_reconnect_secs": 5,
        "topic": "lora_raw",
        "debug": true,
        "debug_topic": "debug_lora_raw"
      },
      "serial": {
        "enabled": true,
        "name": "lora-raw-network",
        "port": "/dev/ttyUSB0",
        "baud_rate": 9600,
        "stop_bits": 1,
        "parity": "N",
        "byte_size": 8,
        "timeout": 5
      }
    }
    '''
    app_setting = AppSetting().reload(setting, None, is_json_str=True)
    print(type(app_setting.mqtt))
    print(type(app_setting.serial))
    print(type(app_setting.mqtt.enabled))
    print('-' * 30)
    print(SerialSetting().serialize())
    print('-' * 30)
    print(AppSetting().serialize())
