from abc import abstractmethod

from flask_restful import marshal_with, reqparse
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.models.model_point import PointModel
from src.resources.model_fields import point_fields_only, point_fields


class PointsPlural(RubixResource):
    @marshal_with(point_fields)
    def get(self):
        return PointModel.find_all()


class PointsBaseSingular(RubixResource):
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
            raise NotFoundException('Point is not found')
        return point

    @classmethod
    @marshal_with(point_fields_only)
    def patch(cls, **kwargs):
        data = PointsBaseSingular.parser.parse_args()
        point: PointModel = cls.get_point(**kwargs)
        if not point:
            raise NotFoundException(f"Does not exist {kwargs}")
        PointModel.filter_by_uuid(point.uuid).update(data)
        PointModel.commit()
        return PointModel.find_by_uuid(point.uuid)

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
