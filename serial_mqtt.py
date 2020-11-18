import json
import logging
import paho.mqtt.client as mqtt
import serial
import sys

CONFIG_FILE = 'config.json'
try:
    with open(CONFIG_FILE) as config_file:
        config = json.load(config_file)
except:
    print("Config file not present or invalid JSON!")
    sys.exit(1)

ser = serial.Serial()
ser.baudrate = config['baudrate']
ser.port = config['port']
ser.timeout = 5

logging.basicConfig(level=logging.DEBUG if config['debug'] else logging.WARNING, format="%(levelname)s: %(message)s")
log = logging.getLogger("")

try:
    ser.open()
    log.info("Worked to open serial port {}!".format(config['port']))
except:
    log.error("Failed to open serial port {}!".format(config['port']))
    import serial.tools.list_ports

    ports = serial.tools.list_ports.comports()
    print("Available serial ports:")
    for port, desc, hwid in sorted(ports):
        print("{}: {}".format(port, desc))
    sys.exit(1)


def on_connect(client, userdata, flags, rc):
    log.info("MQTT on_connect {} {} {} {}".format(client, userdata, flags, rc))


def on_disconnect(client, userdata, rc):
    log.info("MQTT on_disconnect {} {} {}".format(client, userdata, rc))


def on_log(client, userdata, level, buf):
    if level == mqtt.MQTT_LOG_INFO or level == mqtt.MQTT_LOG_NOTICE:
        log.info("MQTT on_log BUF: {}".format(buf))
    elif level == mqtt.MQTT_LOG_WARNING or level == mqtt.MQTT_LOG_ERR:
        log.info("MQTT on_log BUF ERROR: {}".format(buf))


def post_mqtt(topic, message, retain=False):
    log.info("MQTT PUBLISH {} {}".format(topic, message))
    (rc, mid) = mqttc.publish(topic, message, qos=0, retain=retain)
    if rc != mqtt.MQTT_ERR_SUCCESS:
        log.warning("MQTT Publish unsuccessful!")


mqttc = mqtt.Client()

mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_log = on_log

try:
    mqttc.connect(config['mqtt_server'], config['mqtt_port'], 60)
except Exception as e:
    log.error("Can't connect to the MQTT broker! {}".format(e))
    if ser.is_open:
        ser.close()
    sys.exit(1)

mqttc.loop_start()

while True:
    try:
        line = ser.readline().rstrip()
        if line != b'':
            log.debug(line.decode("utf-8"))
            post_mqtt(config['topic'], line)
    except KeyboardInterrupt:
        print('\n')
        mqttc.disconnect()
        if ser.is_open:
            ser.close()
        sys.exit(0)
    except Exception as e:
        log.error("{}".format(e))
        if ser.is_open:
            ser.close()
        sys.exit(1)
