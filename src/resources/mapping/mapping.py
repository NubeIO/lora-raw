import uuid as uuid_

from flask_restful import Resource, marshal_with, abort, reqparse
from sqlalchemy.exc import IntegrityError

from src.models.model_mapping import LPGBPointMapping
from src.resources.model_fields import mapping_lp_gbp_fields


class LPGBPMappingResourceList(Resource):
    @classmethod
    @marshal_with(mapping_lp_gbp_fields)
    def get(cls):
        return LPGBPointMapping.find_all()

    @classmethod
    @marshal_with(mapping_lp_gbp_fields)
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
            data.uuid = str(uuid_.uuid4())
            mapping = LPGBPointMapping(**data)
            mapping.save_to_db()
            # TODO: sync
            return mapping
        except IntegrityError as e:
            abort(400, message=str(e.orig))
        except ValueError as e:
            abort(400, message=str(e))
        except Exception as e:
            abort(500, message=str(e))


class LPGBPMappingResourceBase(Resource):
    @classmethod
    @marshal_with(mapping_lp_gbp_fields)
    def get(cls, uuid):
        mapping = cls.get_mapping(uuid)
        if not mapping:
            abort(404, message=f'Does not exist {uuid}')
        return mapping

    @classmethod
    def delete(cls, uuid):
        mapping = cls.get_mapping(uuid)
        if mapping is None:
            abort(404, message=f'Does not exist {uuid}')
        else:
            mapping.delete_from_db()
        return '', 204


class LPGBPMappingResourceByUUID(LPGBPMappingResourceBase):
    parser = reqparse.RequestParser()
    parser.add_argument('lora_point_uuid', type=str)
    parser.add_argument('generic_point_uuid', type=str, default=None)
    parser.add_argument('bacnet_point_uuid', type=str, default=None)
    parser.add_argument('lora_point_name', type=str)
    parser.add_argument('generic_point_name', type=str, default=None)
    parser.add_argument('bacnet_point_name', type=str, default=None)

    @classmethod
    @marshal_with(mapping_lp_gbp_fields)
    def patch(cls, uuid):
        data = LPGBPMappingResourceByUUID.parser.parse_args()
        mapping = cls.get_mapping(uuid)
        if not mapping:
            abort(404, message='Does not exist {}'.format(uuid))
        try:
            LPGBPointMapping.filter_by_uuid(uuid).update(data)
            LPGBPointMapping.commit()
            # TODO: sync
            return cls.get_mapping(uuid)
        except Exception as e:
            abort(500, message=str(e))

    @classmethod
    def get_mapping(cls, uuid):
        return LPGBPointMapping.find_by_uuid(uuid)


class LPGBPMappingResourceByLoRaPointUUID(LPGBPMappingResourceBase):
    @classmethod
    def get_mapping(cls, uuid):
        return LPGBPointMapping.find_by_lora_point_uuid(uuid)


class LPGBPMappingResourceByGenericPointUUID(LPGBPMappingResourceBase):
    @classmethod
    def get_mapping(cls, uuid):
        return LPGBPointMapping.find_by_generic_point_uuid(uuid)


class LPGBPMappingResourceByBACnetPointUUID(LPGBPMappingResourceBase):
    @classmethod
    def get_mapping(cls, uuid):
        return LPGBPointMapping.find_by_bacnet_point_uuid(uuid)
