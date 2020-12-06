import copy
from flask_restful import reqparse, marshal_with, Resource, abort
from src import db
from src.models.model_serial import SerialDriverModel
from src.resources.mod_fields import serial_driver_field


class SerialDriver(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=int)
    parser.add_argument('port', type=str)
    parser.add_argument('speed', type=int)
    parser.add_argument('stop_bits', type=int)
    parser.add_argument('parity', type=str)
    parser.add_argument('byte_size', type=int)

    @marshal_with(serial_driver_field)
    def get(self):
        return SerialDriverModel.find_one()

    @marshal_with(serial_driver_field)
    def patch(self):
        data = SerialDriver.parser.parse_args()
        data_to_update = {}
        old_serial_driver = copy.deepcopy(SerialDriverModel.find_one())
        for key in data.keys():
            if data[key] is not None:
                data_to_update[key] = data[key]
        SerialDriverModel.query.filter().update(data_to_update)
        new_serial_driver = SerialDriverModel.find_one()
        try:
            # BACServer.get_instance().restart_bac(old_bacnet_server, new_bacnet_server)
            db.session.commit()
            return new_serial_driver
        except Exception as e:
            db.session.rollback()
            abort(501, message=str(e))
