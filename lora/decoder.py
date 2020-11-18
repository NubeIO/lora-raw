import logging
import configparser
import os

temp_path = os.path.dirname(os.path.abspath(__file__))
part_config = os.path.join(temp_path, "../config.ini")

_config = configparser.ConfigParser()
_config.read(part_config)
config_debug = _config.get("debug", "debug")
print(config_debug)


logging.basicConfig(level=logging.DEBUG if config_debug else logging.WARNING, format="%(levelname)s: %(message)s")
log = logging.getLogger("")

# data = 'AAB296C4E5094228BA0000EC0000009A2D64\r'

# log.info("data dump {}".format(data))


class LoRaV1DropletDecoder:
    def __init__(self, _data):
        self._data = _data
        self._data_length = len(_data)

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
        if dl == 36 or dl == 32 or dl == 44: #TODO size 32 is for the old droplets needs to be removed
            return True
        else:
            return False

    def check_sensor_type(self):
        type_aa = "AA"
        type_b0 = "B0"
        type_b1 = "B1"
        type_b2 = "B2"
        type_ab = "AB"
        sub = self._data[2:4]
        if sub == type_aa:
            return type_aa
        elif sub == type_b0:
            return type_b0
        elif sub == type_b1:
            return type_b1
        elif sub == type_b2:
            return type_b2
        elif sub == type_ab:
            return type_ab

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
        return {'id': decode_id, 'pressure': decode_pressure,
                'temp': decode_temp, 'humidity': decode_humidity,
                'voltage': decode_voltage, 'rssi': decode_rssi, 'snr': decode_snr}


# if data is None:
#     log.info("data is none")

# { id: 'AAB296C4',
#   temp: 25.33,
#   pressure: 1030.6,
#   humidity: 58,
#   voltage: 4.72,
#   rssi: -45,
#   snr: 10 }
