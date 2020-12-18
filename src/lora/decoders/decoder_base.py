import logging


logger = logging.getLogger(__name__)


class DecoderBase:

    def __init__(self, data):
        self.data = data
        self.data_length = len(data)

    def set_data(self, data: str):
        self.data = data
        self.data_length = len(data)

    @classmethod
    def check_payload_len(cls, data: str):
        dl = len(data)
        return dl == 36 or dl == 32 or dl == 44  # TODO size 32 is for the old droplets needs to be removed

    def decode_id(self):
        return self.data[0:8]

    def decode_rssi(self):
        a = self.data_length - 4
        b = self.data_length - 2
        x = self.data[a:b]
        x = int(x, 16) * -1
        return x

    def decode_snr(self):
        a = self.data_length - 2
        b = self.data_length
        x = self.data[a:b]
        x = int(x, 16) / 10
        return x

    def decode(self) -> dict:
        rssi = self.decode_rssi()
        snr = self.decode_snr()
        payload = {
            'rssi': rssi,
            'snr': snr,
        }
        return payload
