from src.lora.decoders.decoder_base import DecoderBase


class MicroEdgeDecoderV2(DecoderBase):

    def decode_pulses(self):
        x = int(self.data[8:16], 16)
        return x

    def decode_ai1(self):
        x = int(self.data[18:22], 16)
        return x

    def decode_ai2(self):
        x = int(self.data[22:26], 16)
        return x

    def decode_ai3(self):
        x = int(self.data[26:30], 16)
        return x

    def decode_voltage(self):
        x = int(self.data[16:18], 16) / 50
        return x

    def decode(self) -> dict:
        pulses = self.decode_pulses()
        ai1 = self.decode_ai1()
        ai2 = self.decode_ai2()
        ai3 = self.decode_ai3()
        voltage = self.decode_voltage()
        payload = super().decode()
        payload.update({
            'pulses': pulses,
            'AI1': ai1,
            'AI2': ai2,
            'AI3': ai3,
            'voltage': voltage,
        })
        return payload
