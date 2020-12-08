class LoRaV1DropletDecoder:
    def __init__(self, data):
        self.__data = data
        self.__data_length = len(data)

    def decode_id(self):
        return self.__data[0:8]

    def decode_pressure(self):
        x = self.__data[14:16]
        y = self.__data[12:14]
        out = int(x + y, 16) / 10
        return out

    def decode_temp(self):
        x = self.__data[10:12]
        y = self.__data[8:10]
        out = int(x + y, 16) / 100
        return out

    def decode_humidity(self):
        x = self.__data[14:18]
        out = int(x, 16) % 128
        return out

    def decode_voltage(self):
        x = self.__data[22:24]
        out = int(x, 16) / 50
        return out

    def decode_rssi(self):
        a = self.__data_length - 4
        b = self.__data_length - 2
        x = self.__data[a:b]
        x = int(x, 16)
        out = x * -1
        return out

    def decode_snr(self):
        a = self.__data_length - 2
        b = self.__data_length
        x = self.__data[a:b]
        x = int(x, 16)
        out = x / 10
        return int(out)

    def check_payload_len(self):
        dl = self.__data_length
        return dl == 36 or dl == 32 or dl == 44  # TODO size 32 is for the old droplets needs to be removed

    def check_sensor_type(self):
        supported_sensor_type = ["AA", "B0", "B1", "B2", "AB"]
        sub = self.__data[2:4]
        if sub in supported_sensor_type:
            return sub
        return None

    def data_len(self):
        return self.__data_length

    def decode_all(self):
        decode_pressure = LoRaV1DropletDecoder.decode_pressure(self)
        decode_temp = LoRaV1DropletDecoder.decode_temp(self)
        decode_humidity = LoRaV1DropletDecoder.decode_humidity(self)
        decode_voltage = LoRaV1DropletDecoder.decode_voltage(self)
        decode_rssi = LoRaV1DropletDecoder.decode_rssi(self)
        decode_snr = LoRaV1DropletDecoder.decode_snr(self)
        return {
            'pressure': decode_pressure,
            'temp': decode_temp,
            'humidity': decode_humidity,
            'voltage': decode_voltage,
            'rssi': decode_rssi,
            'snr': decode_snr
        }
