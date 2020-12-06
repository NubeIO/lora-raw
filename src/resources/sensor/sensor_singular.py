import copy

from flask_restful import abort, marshal_with, reqparse

# from src.bac_server import BACServer
from src.models.model_sensor import SensorModel
# from src.models.model_priority_array import PriorityArrayModel
from src.resources.mod_fields import point_fields
from src.resources.point.sensor_base import BACnetPointBase


class BACnetPointSingular(BACnetPointBase):
    parser_patch = reqparse.RequestParser()
    # parser_patch.add_argument('object_type', type=str, required=False)
    parser_patch.add_argument('address', type=int, required=False)
    parser_patch.add_argument('id', type=str, required=True)
    parser_patch.add_argument('sensor_type', type=str, required=True)
    parser_patch.add_argument('sensor_model', type=str, required=True)
    parser_patch.add_argument('micro_edge_input_type', type=str)
    parser_patch.add_argument('sensor_wake_up_rate', type=int, required=False)
    parser_patch.add_argument('units', type=str, required=False)
    parser_patch.add_argument('description', type=str, required=False)
    parser_patch.add_argument('enable', type=bool, required=False)
    parser_patch.add_argument('fault', type=int, required=False)
    parser_patch.add_argument('data_round', type=int, required=False)
    parser_patch.add_argument('data_offset', type=float, required=False)



    @marshal_with(point_fields)
    def get(self, uuid):
        point = SensorModel.find_by_uuid(uuid)
        if not point:
            abort(404, message='BACnet Point is not found')
        return point

    @marshal_with(point_fields)
    def patch(self, uuid):
        data = BACnetPointSingular.parser_patch.parse_args()
        point = copy.deepcopy(SensorModel.find_by_uuid(uuid))
        self.abort_if_bacnet_is_not_running()
        if point is None:
            abort(404, message=f"Does not exist {uuid}")
        try:
            # priority_array_write = data.pop('priority_array_write')
            non_none_data = {}
            for key in data.keys():
                if data[key] is not None:
                    non_none_data[key] = data[key]
            SensorModel.filter_by_uuid(uuid).update(non_none_data)
            # if priority_array_write:
            #     PriorityArrayModel.filter_by_point_uuid(uuid).update(priority_array_write)
            # BACServer.get_instance().remove_point(point)
            point_return = SensorModel.find_by_uuid(uuid)
            # BACServer.get_instance().add_point(point_return)
            return point_return
        except Exception as e:
            abort(500, message=str(e))

    def delete(self, uuid):
        point = SensorModel.find_by_uuid(uuid)
        if point:
            # BACServer.get_instance().remove_point(point)
            point.delete_from_db()
        return '', 204
