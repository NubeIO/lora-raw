from flask_restful import Resource, marshal_with, abort, reqparse
from sqlalchemy.exc import IntegrityError

from src.models.model_mapping import LPGBPointMapping
from src.resources.mod_fields import lp_gbp_mapping_fields


class LPGBPMappingResourceList(Resource):
    @classmethod
    @marshal_with(lp_gbp_mapping_fields)
    def get(cls):
        return LPGBPointMapping.find_all()

    @classmethod
    @marshal_with(lp_gbp_mapping_fields)
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('lora_point_uuid', type=str, required=True)
        parser.add_argument('generic_point_uuid', type=str, default=None)
        parser.add_argument('bacnet_point_uuid', type=str, default=None)
        parser.add_argument('lora_point_name', type=str, required=True)
        parser.add_argument('generic_point_name', type=str, default=None)
        parser.add_argument('bacnet_point_name', type=str, default=None)
        try:
            data = parser.parse_args()
            mapping = LPGBPointMapping(**data)
            mapping.save_to_db()
            return mapping
        except IntegrityError as e:
            abort(400, message=str(e.orig))
        except ValueError as e:
            abort(400, message=str(e))
        except Exception as e:
            abort(500, message=str(e))


class LPGBPMappingResourceBase(Resource):
    @classmethod
    @marshal_with(lp_gbp_mapping_fields)
    def get(cls, point_uuid):
        mapping = cls.get_mapping(point_uuid)
        if not mapping:
            abort(404, message=f'Does not exist {point_uuid}')
        return mapping

    @classmethod
    def delete(cls, point_uuid):
        mapping = cls.get_mapping(point_uuid)
        if mapping is None:
            abort(404, message=f'Does not exist {point_uuid}')
        else:
            mapping.delete_from_db()
        return '', 204


class LPGBPMappingResourceByLoRaPointUUID(LPGBPMappingResourceBase):
    @classmethod
    def get_mapping(cls, point_uuid):
        return LPGBPointMapping.find_by_lora_point_uuid(point_uuid)


class LPGBPMappingResourceByGenericPointUUID(LPGBPMappingResourceBase):
    @classmethod
    def get_mapping(cls, point_uuid):
        return LPGBPointMapping.find_by_generic_point_uuid(point_uuid)


class LPGBPMappingResourceByBACnetPointUUID(LPGBPMappingResourceBase):
    @classmethod
    def get_mapping(cls, point_uuid):
        return LPGBPointMapping.find_by_bacnet_point_uuid(point_uuid)
