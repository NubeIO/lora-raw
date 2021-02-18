from abc import abstractmethod

from flask_restful import Resource, marshal_with, abort, reqparse

from src.models.model_point import PointModel
from src.resources.model_fields import point_fields_only, point_fields


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

    @classmethod
    @marshal_with(point_fields)
    def get(cls, **kwargs):
        point: PointModel = cls.get_point(**kwargs)
        if not point:
            abort(404, message='Point is not found')
        return point

    @classmethod
    @marshal_with(point_fields_only)
    def patch(cls, **kwargs):
        data = PointsBaseSingular.parser.parse_args()
        point: PointModel = cls.get_point(**kwargs)
        if point is None:
            abort(404, message="Does not exist {}".format(kwargs))
        try:
            PointModel.filter_by_uuid(point.uuid).update(data)
            PointModel.commit()
            return PointModel.find_by_uuid(point.uuid)
        except Exception as e:
            abort(500, message=str(e))

    @classmethod
    @abstractmethod
    def get_point(cls, value) -> PointModel:
        raise NotImplementedError('Need to implement')


class PointsSingularByUUID(PointsBaseSingular):
    @classmethod
    def get_point(cls, **kwargs) -> PointModel:
        return PointModel.find_by_uuid(kwargs.get('uuid'))


class PointsSingularByName(PointsBaseSingular):
    @classmethod
    def get_point(cls, **kwargs) -> PointModel:
        return PointModel.find_by_name(kwargs.get('device_name'), kwargs.get('point_name'))
