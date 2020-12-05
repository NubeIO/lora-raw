
def run_decoder(droplet, droplet_list, log):
    payload = None
    if droplet.check_payload_len():
        log.info("check_payload_len {}".format(droplet.check_payload_len()))
        if droplet.check_sensor_type():
            log.info("check_sensor_type {}".format(droplet.check_sensor_type()))
            s = droplet_list
            if droplet.decode_id() in s:
                d_code = droplet.decode_all()
                payload = d_code
                return payload
            else:
                log.warning("droplet_list {} {}".format(droplet_list, droplet.decode_id()))
                return payload
        else:
            log.warning("check_sensor_type {} {}".format(droplet.check_payload_len(), droplet.decode_id()))
            return payload
    else:
        log.warning("check_payload_len {}".format(droplet.check_payload_len()))
        return payload



