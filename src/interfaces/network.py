from enum import Enum


class SerialParity(Enum):
    N = 0
    O = 1
    E = 2


class SupportedFirmwareVersion(Enum):
    v1 = 1
    # v2_encryption = 2
    # v2_non_encryption = 3
