import copy
from flask_restful import marshal_with, abort, reqparse
from src.models.model_sensor import SensorModel
from src.resources.mod_fields import sensor_fields
from src.resources.sensor.sensor_base import SensorBase


class SensorName(SensorBase):
    parser_patch = reqparse.RequestParser()
    parser_patch.add_argument('address', type=int, required=False)
    parser_patch.add_argument('id', type=str, required=True)
    parser_patch.add_argument('sensor_type', type=str, required=True)
    parser_patch.add_argument('sensor_model', type=str, required=True)
    parser_patch.add_argument('micro_edge_input_type', type=str, required=False)
    parser_patch.add_argument('sensor_wake_up_rate', type=int, required=False)
    parser_patch.add_argument('description', type=str, required=False)
    parser_patch.add_argument('enable', type=bool, required=False)
    parser_patch.add_argument('fault', type=int, required=False)
    parser_patch.add_argument('data_round', type=int, required=False)
    parser_patch.add_argument('data_offset', type=float, required=False)

    @marshal_with(sensor_fields)
    def get(self, object_name):
        s = SensorModel.find_by_object_name(object_name)
        if not s:
            abort(404, message='LoRa Sensor is not found')
        return s

    @marshal_with(sensor_fields)
    def patch(self, object_name):
        data = SensorName.parser_patch.parse_args()
        sensor = SensorModel.find_by_object_name(object_name)
        if sensor is None:
            abort(404, message=f"Does not exist {object_name}")
        try:
            non_none_data = {}
            for key in data.keys():
                if data[key] is not None:
                    non_none_data[key] = data[key]
            SensorModel.filter_by_uuid(sensor.uuid).update(non_none_data)
            sensor_return = SensorModel.find_by_uuid(sensor.uuid)
            return sensor_return
        except Exception as e:
            abort(500, message=str(e))
