import copy
from flask_restful import abort, marshal_with, reqparse
from src.models.model_sensor import SensorModel
from src.resources.mod_fields import sensor_fields
from src.resources.sensor.sensor_base import SensorBase


class SensorSingular(SensorBase):
    parser_patch = reqparse.RequestParser()
    parser_patch.add_argument('address', type=int, required=False)
    parser_patch.add_argument('id', type=str, required=True)
    parser_patch.add_argument('sensor_type', type=str, required=True)
    parser_patch.add_argument('sensor_model', type=str, required=True)
    parser_patch.add_argument('micro_edge_input_type', type=str)
    parser_patch.add_argument('sensor_wake_up_rate', type=int, required=False)
    parser_patch.add_argument('description', type=str, required=False)
    parser_patch.add_argument('enable', type=bool, required=False)
    parser_patch.add_argument('fault', type=int, required=False)
    parser_patch.add_argument('data_round', type=int, required=False)
    parser_patch.add_argument('data_offset', type=float, required=False)



    @marshal_with(sensor_fields)
    def get(self, uuid):
        s = SensorModel.find_by_uuid(uuid)
        if not s:
            abort(404, message='LoRa Sensor is not found')
        return s

    @marshal_with(sensor_fields)
    def patch(self, uuid):
        data = SensorSingular.parser_patch.parse_args()
        s = copy.deepcopy(SensorModel.find_by_uuid(uuid))
        self.abort_if_serial_is_not_running()
        if s is None:
            abort(404, message=f"Does not exist {uuid}")
        try:
            non_none_data = {}
            for key in data.keys():
                if data[key] is not None:
                    non_none_data[key] = data[key]
            SensorModel.filter_by_uuid(uuid).update(non_none_data)
            s_return = SensorModel.find_by_uuid(uuid)
            return s_return
        except Exception as e:
            abort(500, message=str(e))

    def delete(self, uuid):
        s = SensorModel.find_by_uuid(uuid)
        if s:
            s.delete_from_db()
        return '', 204
