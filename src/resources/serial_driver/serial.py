from flask_restful import reqparse, marshal_with, Resource, abort

from src.lora.serial_connection_listener import SerialConnectionListener
from src.models.model_serial import SerialDriverModel
from src.resources.mod_fields import serial_driver_field


class SerialDriver(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('port', type=str)
    parser.add_argument('baud_rate', type=int)
    parser.add_argument('stop_bits', type=int)
    parser.add_argument('parity', type=str)
    parser.add_argument('byte_size', type=int)
    parser.add_argument('timeout', type=int)

    @marshal_with(serial_driver_field)
    def get(self):
        return SerialDriverModel.find_one()

    @marshal_with(serial_driver_field)
    def patch(self):
        data = SerialDriver.parser.parse_args()
        data_to_update = {}
        for key in data.keys():
            if data[key] is not None:
                data_to_update[key] = data[key]
        try:
            SerialDriverModel.filter_one().update(data_to_update)
            new_serial_driver = SerialDriverModel.find_one()
            SerialDriverModel.commit()
            SerialConnectionListener.get_instance().restart(new_serial_driver)
            return new_serial_driver
        except Exception as e:
            abort(500, message=str(e))
