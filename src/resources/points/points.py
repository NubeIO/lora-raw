from flask_restful import Resource, marshal_with, abort, reqparse

from src.models.model_point import PointModel
from src.resources.mod_fields import point_fields_only


class PointsResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, store_missing=False)
    parser.add_argument('device_point_name', type=str, store_missing=False)
    parser.add_argument('device_uuid', type=str, store_missing=False)
    parser.add_argument('enable', type=bool, store_missing=False)
    parser.add_argument('cov_threshold', type=int, store_missing=False)
    parser.add_argument('value_round', type=int, store_missing=False)
    parser.add_argument('value_offset', type=int, store_missing=False)
    parser.add_argument('value_operation', type=str, store_missing=False)
    parser.add_argument('input_min', type=int, store_missing=False)
    parser.add_argument('input_max', type=int, store_missing=False)
    parser.add_argument('scale_min', type=int, store_missing=False)
    parser.add_argument('scale_max', type=int, store_missing=False)

    @classmethod
    @marshal_with(point_fields_only)
    def put(cls, value):
        data = PointsResource.parser.parse_args()
        try:
            PointModel.filter_by_uuid(value).update(data)
            PointModel.commit()
            point = PointModel.find_by_uuid(value)
            return point
        except Exception as e:
            abort(500, message=str(e))



