import logging

from src.lora.decoders.decoder_base import DecoderBase

logger = logging.getLogger(__name__)


class DropletDecoderTH(DecoderBase):

    def decode_pressure(self):
        s = self.data[14:16] + self.data[12:14]
        x = int(s, 16) / 10
        return x

    def decode_temperature(self):
        s = self.data[10:12] + self.data[8:10]
        x = int(s, 16) / 100
        return x

    def decode_humidity(self):
        x = int(self.data[16:18], 16) & 127
        return x

    def decode_voltage(self):
        x = int(self.data[22:24], 16) / 50
        return x

    def decode(self) -> dict:
        pressure = self.decode_pressure()
        temperature = self.decode_temperature()
        humidity = self.decode_humidity()
        voltage = self.decode_voltage()
        payload = super().decode()
        payload.update({
            'pressure': pressure,
            'temperature': temperature,
            'humidity': humidity,
            'voltage': voltage
        })
        return payload


class DropletDecoderTHL(DropletDecoderTH):

    def decode_light(self):
        s = self.data[20:22] + self.data[18:20]
        x = int(s, 16)
        return x

    def decode(self) -> dict:
        light = self.decode_light()
        payload = super().decode()
        payload.update({
            'light': light,
        })
        return payload


class DropletDecoderTHLM(DropletDecoderTHL):

    def decode_motion(self):
        x = int(self.data[16:18], 16) > 127
        return x

    def decode(self) -> dict:
        motion = self.decode_motion()
        payload = super().decode()
        payload.update({
            'motion': motion,
        })
        return payload


class DropletDecoderTHA(DropletDecoderTH):

    def decode_airflow(self):
        # TODO: implement
        return 0

    def decode_duct_temperature(self):
        # TODO: implement
        return 0

    def decode_duct_humidity(self):
        # TODO: implement
        return 0

    def decode_self(self):
        airflow = self.decode_airflow()
        duct_temperature = self.decode_duct_temperature()
        duct_humidity = self.decode_duct_humidity()
        return {
            'airflow': airflow,
            'duct_temperature': duct_temperature,
            'duct_humidity': duct_humidity,
        }

    def decode(self) -> dict:
        payload = super().decode()
        payload.update(self.decode_self())
        return payload


class DropletDecoderTHA(DropletDecoderTHL, DropletDecoderTHA):

    def decode(self) -> dict:
        payload = super(DropletDecoderTHL).decode()
        payload.update(super(DropletDecoderTHA).decode_self())
        return payload
