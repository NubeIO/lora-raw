import logging
import enum

from src.lora.decoders.decoder_base import DecoderBase
from src.lora.decoders.dropet_decoder import DropletDecoderTH, DropletDecoderTHL, DropletDecoderTHLM

logger = logging.getLogger(__name__)


class SensorTypes(enum.Enum):
    MICRO_AA = "AA"
    DROPLET_AB = "AB"
    DROPLET_B0 = "B0"
    DROPLET_B1 = "B1"
    DROPLET_B2 = "B2"


class DecoderFactory:

    @staticmethod
    def get_decoder(data: str) -> DecoderBase or None:
        sub = data[2:4]
        try:
            if sub == SensorTypes.MICRO_AA.value:
                raise NotImplementedError
            if sub == SensorTypes.DROPLET_AB.value:
                raise NotImplementedError
            if sub == SensorTypes.DROPLET_B0.value:
                return DropletDecoderTH(data)
            if sub == SensorTypes.DROPLET_B1.value:
                return DropletDecoderTHL(data)
            if sub == SensorTypes.DROPLET_B2.value:
                return DropletDecoderTHLM(data)
        except NotImplementedError:
            logger.warning("No decoder implemented for sensor {}".format(sub))
        return None
