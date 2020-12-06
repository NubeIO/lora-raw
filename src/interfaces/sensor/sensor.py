import enum

class SensorType(enum.Enum):
    DROPLET = 1
    MICRO_EDGE = 2
    IO_10 = 3


class SensorModel(enum.Enum):
    MICRO_EDGE = 1
    DROPLET_TH = 2
    DROPLET_THL = 3
    DROPLET_THML = 4


class MicroEdgeInputType(enum.Enum):
    TEMP_10K = 1
    VOLTAGE = 2
    DIGITAL = 3


class EventState(enum.Enum):
    normal = 0,
    fault = 1,