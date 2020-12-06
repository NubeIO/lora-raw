import uuid

from flask_restful import marshal_with

# from src.bac_server import BACServer
from src.models.model_sensor import SensorModel
# from src.models.model_priority_array import PriorityArrayModel
from src.resources.mod_fields import sensor_fields
from src.resources.sensor.sensor_base import SensorBase


class SensorPlural(SensorBase):
    @marshal_with(sensor_fields, envelope="points")
    def get(self):
        return SensorModel.query.all()

    @marshal_with(sensor_fields)
    def post(self):
        _uuid = str(uuid.uuid4())
        data = SensorPlural.parser.parse_args()
        return self.add_point(data, _uuid)

    def delete(self):
        SensorModel.delete_all_from_db()
        return '', 204
