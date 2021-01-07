from enum import Enum, auto


class DeviceTypes(Enum):
    DROPLET = auto()
    MICRO_EDGE = auto()


class DeviceModels(Enum):
    MICRO_EDGE = auto()
    DROPLET_TH = auto()
    DROPLET_THL = auto()
    DROPLET_THLM = auto()
    DROPLET_THA = auto()
    DROPLET_THLA = auto()


def verify_device_model(dev_type: DeviceTypes, model: DeviceModels) -> bool:
    if dev_type is DeviceTypes.MICRO_EDGE:
        return model is DeviceModels.MICRO_EDGE
    elif model is DeviceModels.MICRO_EDGE:
        return False
    return True
