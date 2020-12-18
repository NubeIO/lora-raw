from flask_restful import abort, marshal_with, reqparse

from src.models.model_sensor import SensorModel
from src.resources.mod_fields import sensor_fields
from src.resources.sensor.sensor_base import SensorBase


class SensorSingular(SensorBase):
    parser_patch = reqparse.RequestParser()
    parser_patch.add_argument('name', type=str)
    parser_patch.add_argument('sensor_type', type=str)
    parser_patch.add_argument('sensor_model', type=str)
    parser_patch.add_argument('micro_edge_input_type', type=str)
    parser_patch.add_argument('sensor_wake_up_rate', type=int)
    parser_patch.add_argument('description', type=str)
    parser_patch.add_argument('enable', type=bool)
    parser_patch.add_argument('fault', type=int)
    parser_patch.add_argument('data_round', type=int)
    parser_patch.add_argument('data_offset', type=float)

    @marshal_with(sensor_fields)
    def get(self, uuid):
        sensor = SensorModel.find_by_uuid(uuid)
        if not sensor:
            abort(404, message='LoRa Sensor is not found')
        return sensor

    @marshal_with(sensor_fields)
    def patch(self, uuid):
        data = SensorSingular.parser_patch.parse_args()
        sensor = SensorModel.find_by_uuid(uuid)
        if sensor is None:
            abort(404, message="Does not exist {}".format(uuid))
        try:
            non_none_data = {}
            for key in data.keys():
                if data[key] is not None:
                    non_none_data[key] = data[key]
            return self.update_sensor(uuid, non_none_data)
        except Exception as e:
            abort(500, message=str(e))

    def delete(self, uuid):
        sensor = SensorModel.find_by_uuid(uuid)
        if sensor:
            sensor.delete_from_db()
        return '', 204
