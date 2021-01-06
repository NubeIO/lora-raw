from flask_restful import reqparse, marshal_with, Resource, abort

from src.lora import SerialConnectionListener
from src.models.model_network import NetworkModel
from src.resources.mod_fields import network_fields


class SerialDriver(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('port', type=str)
    parser.add_argument('baud_rate', type=int)
    parser.add_argument('stop_bits', type=int)
    parser.add_argument('parity', type=str)
    parser.add_argument('byte_size', type=int)
    parser.add_argument('timeout', type=int)
    parser.add_argument('firmware_version', type=str)
    parser.add_argument('encryption_key', type=str)

    @marshal_with(network_fields)
    def get(self):
        return NetworkModel.find_one()

    @marshal_with(network_fields)
    def patch(self):
        data = SerialDriver.parser.parse_args()
        data_to_update = {}
        for key in data.keys():
            if data[key] is not None:
                data_to_update[key] = data[key]
        try:
            NetworkModel.filter_one().update(data_to_update)
            new_serial_driver = NetworkModel.find_one()
            NetworkModel.commit()
            SerialConnectionListener().restart(new_serial_driver)
            return new_serial_driver
        except Exception as e:
            abort(500, message=str(e))
