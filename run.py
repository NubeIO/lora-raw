import configparser
import json
import logging
import os

import paho.mqtt.client as mqtt
import serial
import sys
from lora.decoder import LoRaV1DropletDecoder
from lora.clean_payload import CleanPayload
from lora.run_decoder import run_decoder

temp_path = os.path.dirname(os.path.abspath(__file__))
part_config = os.path.join(temp_path, "config.ini")

print(part_config)

config = configparser.ConfigParser()
config.read(part_config)
config_debug = config.get("debug", "debug")
config_baudrate = config.get("serial", "baudrate")
config_port = config.get("serial", "port")
config_sensor_list = config.get("sensor_list", "sensor_list")

config_broker = config.get("mqtt", "broker")
config_mqtt_port = config.get("mqtt", "mqtt_port")
config_mqtt_port = int(config_mqtt_port)
config_topic = config.get("mqtt", "topic")

ser = serial.Serial()
ser.baudrate = config_baudrate
ser.port = config_port
ser.timeout = 5

logging.basicConfig(level=logging.DEBUG if config_debug else logging.WARNING, format="%(levelname)s: %(message)s")
log = logging.getLogger("")
#
try:
    ser.open()
    log.info("Worked to open serial port {}!".format(config_port))
except:
    log.error("Failed to open serial port {}!".format(config_port))
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
    # client.publish("topic", , qos=2, retain=False)
    (rc, mid) = mqttc.publish(topic, payload=json.dumps(message), qos=0, retain=retain)
    if rc != mqtt.MQTT_ERR_SUCCESS:
        log.warning("MQTT Publish unsuccessful!")


mqttc = mqtt.Client()

mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_log = on_log

try:
    mqttc.connect(config_broker, config_mqtt_port, 60)
except Exception as e:
    log.error("Can't connect to the MQTT broker! {}".format(e))
    if ser.is_open:
        ser.close()
    sys.exit(1)

mqttc.loop_start()

# if payload is not None:
#     log.info("payload {}".format(payload))


while True:
    try:
        line = ser.readline().rstrip()
        if line != b'':
            log.debug(line.decode("utf-8"))
            data = line.decode('utf-8')
            log.info("pre_clean_data {}".format({"pre_clean_data": data, "data_len": len(data)}))
            data = CleanPayload(data)
            data = data.clean_data()
            droplet = LoRaV1DropletDecoder(data)
            log.info("after clean {}".format(
                {"after_clean_data": data, "data_len": len(data), "check_len": droplet.check_payload_len()}))
            data_length = droplet.data_len()
            sensorType = 'droplet'
            droplet_list = config_sensor_list
            log.info("droplet_list{}".format(droplet_list))
            payload = run_decoder(droplet, droplet_list, log)
            log.info("MQTT PAYLOAD {}".format(payload))
            if payload is not None:
                post_mqtt(config_topic, payload)
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
