from abc import abstractmethod

from flask_restful import Resource, marshal_with, abort, reqparse

from src.models.model_point import PointModel
from src.resources.mod_fields import point_fields_only, point_fields


class PointsPlural(Resource):
    @marshal_with(point_fields)
    def get(self):
        return PointModel.find_all()


class PointsBaseSingular(Resource):
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

    @marshal_with(point_fields_only)
    def patch(self, value):
        data = PointsBaseSingular.parser.parse_args()
        point = self.get_point(value)
        if point.first() is None:
            abort(404, message="Does not exist {}".format(value))
        try:
            uuid = point.first().uuid
            point.update(data)
            PointModel.commit()
            return PointModel.find_by_uuid(uuid)
        except Exception as e:
            abort(500, message=str(e))

    @abstractmethod
    def get_point(self, value):
        raise NotImplementedError('Need to implement')


class PointsSingularByUUID(PointsBaseSingular):
    def get_point(self, value):
        return PointModel.filter_by_uuid(value)


class PointsSingularByName(PointsBaseSingular):
    def get_point(self, value):
        return PointModel.filter_by_name(value)
