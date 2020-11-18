import math

data = "C1AB289500B608B4273005DB37234470"


class LoRaV0Decoder:
    def __init__(self, _data):
        self._data = _data
        self._data_length = len(data)

    def decode_id(self):
        x = self._data[0:8]
        out = x
        return out

    def decode_pressure(self):
        x = self._data[16:18]
        y = self._data[14:16]
        out = int(x + y, 16) / 10
        return out

    def decode_temp(self):
        x = self._data[12:14]
        y = self._data[10:12]
        out = int(x + y, 16) / 100
        return out

    def decode_humidity(self):
        x = self._data[18:20]
        x = "0x" + x
        x = int(x, 16)
        x = int(x) % 128
        return x

    def decode_voltage(self):
        x = self._data[22:24]
        x = "0x" + x
        x = int(x, 16)
        x = int(x) / 50
        return x

    def decode_rssi(self):
        x = self._data[28:30]
        x = "0x" + x
        x = int(x, 16)
        x = int(x) * -1
        return x

    def decode_snr(self):
        x = self._data[30:32]
        x = "0x" + x
        x = int(x, 16)
        x = int(x) / 10
        return x

    def decode_movement(self):
        x = self._data[20:22]
        x = "0x" + x
        x = int(x, 16)
        x = int(x) > 127
        return x

    def decode_lux(self):
        x = self._data[20:22]
        x = "0x" + x
        x = int(x, 16)
        x = math.pow(x, 2)
        x = int(x)
        return x

    def decode_all(self):
        decode_id = LoRaV0Decoder.decode_id(self)
        decode_pressure = LoRaV0Decoder.decode_pressure(self)
        decode_temp = LoRaV0Decoder.decode_temp(self)
        decode_humidity = LoRaV0Decoder.decode_humidity(self)
        decode_voltage = LoRaV0Decoder.decode_voltage(self)
        decode_rssi = LoRaV0Decoder.decode_rssi(self)
        decode_snr = LoRaV0Decoder.decode_snr(self)
        decode_movement = LoRaV0Decoder.decode_rssi(self)
        decode_lux = LoRaV0Decoder.decode_lux(self)
        return {'decode_id': decode_id, 'decode_pressure': decode_pressure,
                'decode_temp': decode_temp, 'decode_humidity': decode_humidity,
                'decode_voltage': decode_voltage, 'decode_rssi': decode_rssi,
                'decode_snr': decode_snr, 'decode_movement': decode_movement, 'decode_lux': decode_lux}




aa = LoRaV0Decoder(data)
print(aa.decode_all())
