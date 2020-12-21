class DeviceRegistry:
    __instance = None

    def __init__(self):
        if DeviceRegistry.__instance:
            raise Exception("DeviceRegistry class is a singleton class!")
        else:
            self.__devices = {}
            DeviceRegistry.__instance = self

    @staticmethod
    def get_instance():
        if DeviceRegistry.__instance is None:
            DeviceRegistry()
        return DeviceRegistry.__instance

    def get_devices(self):
        return self.__devices

    def get_device(self, device) -> tuple:
        if self.__devices[device]:
            return self.__devices[device]
        return None, None

    def add_device(self, device, uuid, name):
        self.__devices[device] = uuid, name

    def remove_device(self, device):
        self.__devices.pop(device, None)

    def remove_all_devices(self):
        self.__devices = {}
