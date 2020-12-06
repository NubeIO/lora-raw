import uuid

from flask_restful import marshal_with

# from src.bac_server import BACServer
from src.models.model_sensor import SensorModel
# from src.models.model_priority_array import PriorityArrayModel
from src.resources.mod_fields import point_fields
from src.resources.point.sensor_base import BACnetPointBase


class BACnetPointPlural(BACnetPointBase):
    @marshal_with(point_fields, envelope="points")
    def get(self):
        return SensorModel.query.all()

    @marshal_with(point_fields)
    def post(self):
        print(11111)
        # self.abort_if_bacnet_is_not_running()
        print(11111)
        _uuid = str(uuid.uuid4())
        data = BACnetPointPlural.parser.parse_args()
        print(data, _uuid)
        return self.add_point(data, _uuid)

    def delete(self):
        SensorModel.delete_all_from_db()
        # BACServer.get_instance().remove_all_points()
        return '', 204
