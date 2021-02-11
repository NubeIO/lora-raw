from ast import literal_eval
from typing import List

from mrb.mapper import api_to_topic_mapper
from mrb.message import HttpMethod
from sqlalchemy import and_, or_

from src import db, FlaskThread
from src.models.model_mapping import LPGBPointMapping


class PointStoreModelMixin(object):
    value = db.Column(db.Float(), nullable=True)
    value_original = db.Column(db.Float(), nullable=True)
    value_raw = db.Column(db.String(), nullable=True)
    fault = db.Column(db.Boolean(), default=False, nullable=False)
    fault_message = db.Column(db.String())
    ts = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


class PointStoreModel(PointStoreModelMixin, db.Model):
    __tablename__ = 'point_stores'
    point_uuid = db.Column(db.String, db.ForeignKey('points.uuid'), primary_key=True, nullable=False)

    def __repr__(self):
        return f"PointStore(point_uuid = {self.point_uuid})"

    @classmethod
    def find_by_point_uuid(cls, point_uuid: str):
        return cls.query.filter_by(point_uuid=point_uuid).first()

    @classmethod
    def create_new_point_store_model(cls, point_uuid: str):
        return PointStoreModel(point_uuid=point_uuid, value_original=None, value=None, value_raw="")

    def raw_value(self) -> any:
        """Parse value from value_raw"""
        if self.value_raw:
            value_raw = literal_eval(self.value_raw)
            return value_raw
        else:
            return None

    def update(self, cov_threshold: float = None) -> bool:
        if not self.fault:
            self.fault = bool(self.fault)
            res = db.session.execute(
                self.__table__
                    .update()
                    .values(value=self.value,
                            value_original=self.value_original,
                            value_raw=self.value_raw,
                            fault=False,
                            fault_message=None)
                    .where(and_(self.__table__.c.point_uuid == self.point_uuid,
                                or_(self.__table__.c.value == None,
                                    db.func.abs(self.__table__.c.value - self.value) >= cov_threshold,
                                    self.__table__.c.fault != self.fault))))
        else:
            res = db.session.execute(
                self.__table__
                    .update()
                    .values(fault=self.fault, fault_message=self.fault_message)
                    .where(and_(self.__table__.c.point_uuid == self.point_uuid,
                                or_(self.__table__.c.fault != self.fault,
                                    self.__table__.c.fault_message != self.fault_message))))
        db.session.commit()
        updated: bool = bool(res.rowcount)
        if updated:
            FlaskThread(target=self.__sync_point_value, daemon=True).start()
        return updated

    def __sync_point_value(self):
        mapping: LPGBPointMapping = LPGBPointMapping.find_by_lora_point_uuid(self.point_uuid)
        if mapping:
            if mapping.generic_point_uuid:
                api_to_topic_mapper(
                    api=f"/api/generic/points_value/uuid/{mapping.generic_point_uuid}",
                    destination_identifier='ps',
                    body={"priority_array": {"_16": self.value}},
                    http_method=HttpMethod.PATCH)
            elif mapping.bacnet_point_uuid:
                api_to_topic_mapper(
                    api=f"/api/bacnet/points/uuid/{mapping.bacnet_point_uuid}",
                    destination_identifier=f'bacnet',
                    body={"priority_array_write": {"_16": self.value}},
                    http_method=HttpMethod.PATCH)

    @classmethod
    def sync_points_values(cls):
        mappings: List[LPGBPointMapping] = LPGBPointMapping.find_all()
        for mapping in mappings:
            point_store: PointStoreModel = PointStoreModel.find_by_point_uuid(mapping.lora_point_uuid)
            FlaskThread(target=point_store.__sync_point_value, daemon=True).start()
