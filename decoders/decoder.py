import json
import logging
import sys

CONFIG_FILE = '../settings/config.json'
try:
    with open(CONFIG_FILE) as config_file:
        config = json.load(config_file)
except:
    print("Config file not present or invalid JSON!")
    sys.exit(1)

logging.basicConfig(level=logging.DEBUG if config['debug'] else logging.WARNING, format="%(levelname)s: %(message)s")
log = logging.getLogger("")

data = 'AAB296C4E5094228BA0000EC0000009A2D64\r'

log.info("data dump {}".format(data))


class LoRaV1DropletDecoder:
    def __init__(self, _data):
        self._data = _data
        self._data_length = len(data)

    def decode_id(self):
        x = self._data[0:8]
        out = x
        return out

    def decode_pressure(self):
        x = self._data[14:16]
        y = self._data[12:14]
        out = int(x + y, 16) / 10
        return out

    def decode_temp(self):
        x = self._data[10:12]
        y = self._data[8:10]
        out = int(x + y, 16) / 100
        return out

    def decode_humidity(self):
        x = self._data[14:18]
        out = int(x, 16) % 128
        return out

    def decode_voltage(self):
        x = self._data[22:24]
        out = int(x, 16) / 50
        return out

    def decode_rssi(self):
        a = self._data_length - 4
        b = self._data_length - 2
        x = self._data[a:b]
        x = int(x, 16)
        out = x * -1
        return out

    def decode_snr(self):
        a = self._data_length - 2
        b = self._data_length
        x = self._data[a:b]
        x = int(x, 16)
        out = x / 10
        return int(out)

    def check_sensor_is_type(self):
        sub = self._data[2:4]
        if sub != 'AA' and sub != 'B0' and sub != 'B1' and sub != 'B2':
            return True
        else:
            return False

    def check_payload_len(self):
        dl = self._data_length
        if dl == 36 or dl == 44:
            return True
        else:
            return False

    def check_sensor_type(self):
        type_aa = "AA"
        type_b0 = "B0"
        type_b1 = "B1"
        type_b2 = "B2"
        sub = self._data[2:4]
        if sub == type_aa:
            return type_aa
        elif sub == type_b0:
            return type_b0
        elif sub == type_b1:
            return type_b1
        elif sub == type_b2:
            return type_b2

    def data_len(self):
        return len(self._data)

    def decode_all(self):
        decode_id = LoRaV1DropletDecoder.decode_id(self)
        decode_pressure = LoRaV1DropletDecoder.decode_pressure(self)
        decode_temp = LoRaV1DropletDecoder.decode_temp(self)
        decode_humidity = LoRaV1DropletDecoder.decode_humidity(self)
        decode_voltage = LoRaV1DropletDecoder.decode_voltage(self)
        decode_rssi = LoRaV1DropletDecoder.decode_rssi(self)
        decode_snr = LoRaV1DropletDecoder.decode_snr(self)
        return {'decode_id': decode_id, 'decode_pressure': decode_pressure,
                'decode_temp': decode_temp, 'decode_humidity': decode_humidity,
                'decode_voltage': decode_voltage, 'decode_rssi': decode_rssi, 'decode_snr': decode_snr}


def clean_data(_data):
    """
    cleans the payload data removes '\n' from the string
    :param _data: string
    :return: string
    """
    d = _data
    dl = len(_data)
    if dl % 2 == 1 and (d[dl - 1] == '\r' or d[dl - 1] == '\n'):
        d = d[0:dl - 1]
        return d
    elif d[dl - 2:dl] == '\r\n':
        d = d[0:dl - 2]
        return d
    else:
        return d


if data is None:
    log.info("data is none")

log.info("pre_clean_data {}".format({"pre_clean_data": data, "data_len": len(data)}))
data = clean_data(data)
droplet = LoRaV1DropletDecoder(data)
log.info("after clean {}".format(
    {"after_clean_data": data, "data_len": len(data), "check_len": droplet.check_payload_len()}))

data_length = droplet.data_len()

sensorType = 'droplet'

# nodeID = 'AAB296C4'.upper() or ''

droplet_list = {'AAB296C4', 'AAB296C4'}

payload = None
if droplet.check_payload_len():
    log.info("check_payload_len {}".format(droplet.check_payload_len()))
    if droplet.check_sensor_type():
        log.info("check_sensor_type {}".format(droplet.check_sensor_type()))
        s = droplet_list
        if droplet.decode_id() in s:
            d_code = droplet.decode_all()
            payload = d_code
            log.info("decode_all {}".format(d_code))
        else:
            log.warning("droplet_list {} {}".format(droplet_list, droplet.decode_id()))
    else:
        log.warning("check_sensor_type {} {}".format(droplet.check_payload_len(), droplet.decode_id()))
else:
    log.warning("check_payload_len {}".format(droplet.check_payload_len()))

# if data_length != 36:
#     print(222)

# print(droplet.check_sensor_type())

# { id: 'AAB296C4',
#   temp: 25.33,
#   pressure: 1030.6,
#   humidity: 58,
#   voltage: 4.72,
#   rssi: -45,
#   snr: 10 }


