from flask_restful import Resource, reqparse, abort
from src.models.model_sensor import SensorModel


class BACnetPointBase(Resource):
    parser = reqparse.RequestParser()
    # parser.add_argument('object_type', type=str)
    parser.add_argument('object_name', type=str)
    parser.add_argument('address', type=int)
    parser.add_argument('id', type=str)
    parser.add_argument('sensor_type', type=str)
    parser.add_argument('sensor_model', type=str)
    parser.add_argument('micro_edge_input_type', type=str)
    parser.add_argument('sensor_wake_up_rate', type=int, required=True)
    parser.add_argument('units', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('enable', type=bool)
    parser.add_argument('fault', type=int)
    parser.add_argument('data_round', type=int)
    parser.add_argument('data_offset', type=float)

    def add_point(self, data, uuid):
        try:
            point = SensorModel(uuid=uuid, **data)
            point.save_to_db()
            return point
        except Exception as e:
            abort(500, message=str(e))

    def abort_if_bacnet_is_not_running(self):
        if not True:
            abort(400, message='Bacnet serial_driver is not running')
        # if not BACServer.get_instance().status():
        #     abort(400, message='Bacnet serial_driver is not running')
