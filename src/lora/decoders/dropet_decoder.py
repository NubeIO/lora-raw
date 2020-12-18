import logging
from math import pow

from src.lora.decoders.decoder_base import DecoderBase

logger = logging.getLogger(__name__)


class DropletDecoderTH(DecoderBase):

    def decode_pressure(self):
        x = self.data[14:16]
        y = self.data[12:14]
        out = int(x + y, 16) / 10
        return out

    def decode_temp(self):
        x = self.data[10:12]
        y = self.data[8:10]
        out = int(x + y, 16) / 100
        return out

    def decode_humidity(self):
        x = self.data[14:18]
        out = int(x, 16) % 128
        return out

    def decode_voltage(self):
        x = self.data[22:24]
        out = int(x, 16) / 50
        return out

    def decode(self) -> dict:
        pressure = self.decode_pressure()
        temp = self.decode_temp()
        humidity = self.decode_humidity()
        voltage = self.decode_voltage()
        payload = super().decode()
        payload.update({
            'pressure': pressure,
            'temp': temp,
            'humidity': humidity,
            'voltage': voltage
        })
        return payload


class DropletDecoderTHL(DropletDecoderTH):

    def decode_lux(self):
        x = self.data[20:22]
        x = int(x, 16)
        x = int(pow(x, 2))
        return x

    def decode(self) -> dict:
        lux = self.decode_lux()
        payload = super().decode()
        payload.update({
            'lux': lux,
        })
        return payload


class DropletDecoderTHLM(DropletDecoderTHL):

    def decode_movement(self):
        x = self.data[20:22]
        x = int(x, 16) > 127
        return x

    def decode(self) -> dict:
        movement = self.decode_movement()
        payload = super().decode()
        payload.update({
            'movement': movement,
        })
        return payload
