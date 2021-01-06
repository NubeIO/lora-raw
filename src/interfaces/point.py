from enum import Enum, auto


class HistoryType(Enum):
    COV = 0,
    INTERVAL = 1


class MathOperation(Enum):
    ADD = 0
    SUBTRACT = 1
    MULTIPLY = 2
    DIVIDE = 3
    BOOL_INVERT = 4


class MicroEdgeInputType(Enum):
    TEMP_10K = auto()
    VOLTAGE = auto()
    DIGITAL = auto()
