from mrb.mapper import api_to_topic_mapper
from mrb.message import HttpMethod, Response
from mrb.validator import is_valid
from sqlalchemy.orm import validates

from src import db
from src.models.model_base import ModelBase


class LPGBPointMapping(ModelBase):
    """
    lora_point <> generic_point | bacnet_point
    """
    __tablename__ = 'lp_gbp_mappings'

    lora_point_uuid = db.Column(db.String, db.ForeignKey('points.uuid'), primary_key=True, nullable=False)
    generic_point_uuid = db.Column(db.String(80), nullable=True, unique=True)
    bacnet_point_uuid = db.Column(db.String(80), nullable=True, unique=True)
    lora_point_name = db.Column(db.String(80), nullable=False)
    generic_point_name = db.Column(db.String(80), nullable=False)
    bacnet_point_name = db.Column(db.String(80), nullable=False)

    @validates('generic_point_uuid')
    def validate_generic_point_uuid(self, _, value):
        if value:
            response: Response = api_to_topic_mapper(api=f'/api/generic/points/{value}',
                                                     destination_identifier=f'ps', http_method=HttpMethod.GET)
            if not is_valid(response):
                raise ValueError(response.message)
        return value

    @validates('bacnet_point_uuid')
    def validate_bacnet_point_uuid(self, _, value):
        if value:
            response: Response = api_to_topic_mapper(api=f'/api/bacnet/points/uuid/{value}',
                                                     destination_identifier=f'bacnet', http_method=HttpMethod.GET)
            if not is_valid(response):
                raise ValueError(response.message)
        return value

    @validates('bacnet_point_name')
    def validate_bacnet_point_name(self, _, value):
        self.validate(value)
        return value

    def validate(self, bacnet_point_name: str):
        if not ((self.generic_point_uuid and not self.bacnet_point_uuid) or (
                not self.generic_point_uuid and self.bacnet_point_uuid)):
            raise ValueError("either generic_point_uuid or bacnet_point_uuid should be mapped")
        if self.generic_point_uuid:
            if not self.generic_point_name:
                raise ValueError("generic_point_name should not be null or blank")
            if bacnet_point_name:
                raise ValueError("bacnet_point_name should be null when generic_point_uuid is not null")
        if self.bacnet_point_uuid:
            if not bacnet_point_name:
                raise ValueError("bacnet_point_name should not be null or blank")
            if self.generic_point_name:
                raise ValueError("generic_point_name should be null when bacnet_point_uuid is not null")
        if not self.lora_point_name:
            raise ValueError("lora_point_name should not be null or blank")

    @classmethod
    def find_by_lora_point_uuid(cls, lora_point_uuid):
        return cls.query.filter_by(lora_point_uuid=lora_point_uuid).first()

    @classmethod
    def find_by_generic_point_uuid(cls, generic_point_uuid):
        return cls.query.filter_by(generic_point_uuid=generic_point_uuid).first()

    @classmethod
    def find_by_bacnet_point_uuid(cls, bacnet_point_uuid):
        return cls.query.filter_by(bacnet_point_uuid=bacnet_point_uuid).first()
