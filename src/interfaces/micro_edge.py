from enum import Enum, auto


class MicroEdgeInputType(Enum):
    TEMPERATURE_10K = auto()
    VDC_0_10 = auto()
    DIGITAL = auto()
