data = 'AAB296C4E5094228BA0000EC0000009A2D64'
print(data)


class LoRaV1Decoder:
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

    def decode_all(self):
        decode_id = LoRaV1Decoder.decode_id(self)
        decode_pressure = LoRaV1Decoder.decode_pressure(self)
        decode_temp = LoRaV1Decoder.decode_temp(self)
        decode_humidity = LoRaV1Decoder.decode_humidity(self)
        decode_voltage = LoRaV1Decoder.decode_voltage(self)
        decode_rssi = LoRaV1Decoder.decode_rssi(self)
        decode_snr = LoRaV1Decoder.decode_snr(self)
        return {'decode_id': decode_id, 'decode_pressure': decode_pressure,
                'decode_temp': decode_temp, 'decode_humidity': decode_humidity,
                'decode_voltage': decode_voltage, 'decode_rssi': decode_rssi, 'decode_snr': decode_snr}


aa = LoRaV1Decoder(data)
print(aa.decode_all())

# { id: 'AAB296C4',
#   temp: 25.33,
#   pressure: 1030.6,
#   humidity: 58,
#   voltage: 4.72,
#   rssi: -45,
#   snr: 10 }


data_length = len(data)



sensorType = 'droplet'

nodeID = 'AAB296C4'.upper() or '';
if data is None:
    print("")

dl_min_1 = data_length - 1
dl_min_2 = data_length - 2
if len(data) % 2 == 1 and (data[len(data) - 1] == '\r' or data[len(data) - 1] == '\n'):
    print("")
    data = data[0:dl_min_1]
elif data[dl_min_2:data_length] == '\r\n':
    print("")
    data = data[0:dl_min_2]
