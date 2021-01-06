from src.utils import Singleton


class DeviceRegistry(metaclass=Singleton):

    def __init__(self):
        self.__devices = {}

    def get_devices(self):
        return self.__devices

    def get_device(self, device_id) -> tuple:
        if device_id in self.__devices.keys():
            return self.__devices[device_id]
        return None

    def add_device(self, device_id, _uuid):
        self.__devices[device_id] = _uuid

    def remove_device(self, device_id):
        self.__devices.pop(device_id, None)

    def remove_all_devices(self):
        self.__devices = {}
