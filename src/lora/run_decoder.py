import logging

from src.lora.decoder import LoRaV1DropletDecoder

logger = logging.getLogger(__name__)


def run_decoder(droplet: LoRaV1DropletDecoder, droplet_list):
    payload = None
    if droplet.check_payload_len():
        logger.info("check_payload_len {}".format(droplet.check_payload_len()))
        if droplet.check_sensor_type():
            logger.info("check_sensor_type {}".format(droplet.check_sensor_type()))
            s = droplet_list
            if droplet.decode_id() in s:
                d_code = droplet.decode_all()
                payload = d_code
                return payload
            else:
                logger.warning("droplet_list {} {}".format(droplet_list, droplet.decode_id()))
                return payload
        else:
            logger.warning("check_sensor_type {} {}".format(droplet.check_payload_len(), droplet.decode_id()))
            return payload
    else:
        logger.warning("check_payload_len {}".format(droplet.check_payload_len()))
        return payload
