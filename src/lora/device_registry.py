from src.utils import Singleton


class DeviceRegistry(metaclass=Singleton):

    def __init__(self):
        self.__devices = {}

    def get_devices(self):
        return self.__devices

    def get_device(self, device) -> tuple:
        if self.__devices[device]:
            return self.__devices[device]
        return None, None

    def add_device(self, device, uuid, name):
        # TODO: wtf???
        self.__devices[device] = uuid, name

    def remove_device(self, device):
        self.__devices.pop(device, None)

    def remove_all_devices(self):
        self.__devices = {}
