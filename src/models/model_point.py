import re

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates

from src import db
from src.interfaces.point import MathOperation
from src.models.model_base import ModelBase
from src.models.model_device import DeviceModel
from src.models.model_network import NetworkModel
from src.models.model_point_store import PointStoreModel


class PointModel(ModelBase):
    __tablename__ = 'points'

    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False, unique=True)
    device_uuid = db.Column(db.String, db.ForeignKey('devices.uuid'), nullable=False)
    enable = db.Column(db.Boolean(), nullable=False, default=True)
    device_point_name = db.Column(db.String(), nullable=False)
    cov_threshold = db.Column(db.Float, nullable=False, default=0)
    value_round = db.Column(db.Integer(), nullable=False, default=2)
    value_offset = db.Column(db.Float(), nullable=False, default=0)
    value_operation = db.Column(db.Enum(MathOperation), nullable=True)
    input_min = db.Column(db.Float())
    input_max = db.Column(db.Float())
    scale_min = db.Column(db.Float())
    scale_max = db.Column(db.Float())
    point_store = db.relationship('PointStoreModel', backref='point', lazy=False, uselist=False, cascade="all,delete")

    __table_args__ = (
        UniqueConstraint('name', 'device_uuid'),
    )

    def __repr__(self):
        return f"Point(uuid = {self.uuid})"

    @validates('name')
    def validate_name(self, _, value):
        if not re.match("^([A-Za-z0-9_-])+$", value):
            raise ValueError("name should be alphanumeric and can contain '_', '-'")
        return value

    @classmethod
    def find_by_name(cls, device_name: str, point_name: str):
        results = cls.query.filter_by(name=point_name) \
            .join(DeviceModel).filter_by(name=device_name) \
            .first()
        return results

    def save_to_db(self):
        self.point_store = PointStoreModel.create_new_point_store_model(self.uuid)
        super().save_to_db()

    def save_to_db_no_commit(self):
        self.point_store = PointStoreModel.create_new_point_store_model(self.uuid)
        super().save_to_db_no_commit()

    def update_point_value(self, point_store: PointStoreModel, cov_threshold: float = None) -> bool:
        if not point_store.fault:
            if cov_threshold is None:
                cov_threshold = self.cov_threshold

            value = point_store.value_original
            if value is not None:
                value = self.apply_scale(value, self.input_min, self.input_max, self.scale_min,
                                         self.scale_max)
                value = self.apply_offset(value, self.value_offset, self.value_operation)
                value = round(value, self.value_round)
            point_store.value = value
        return point_store.update(cov_threshold)

    @classmethod
    def apply_offset(cls, original_value: float, value_offset: float, value_operation: MathOperation) -> float or None:
        """Do calculations on original value with the help of point details"""
        if original_value is None or value_operation is None:
            return original_value
        value = original_value
        if value_operation == MathOperation.ADD:
            value += value_offset
        elif value_operation == MathOperation.SUBTRACT:
            value -= value_offset
        elif value_operation == MathOperation.MULTIPLY:
            value *= value_offset
        elif value_operation == MathOperation.DIVIDE:
            value /= value_offset
        elif value_operation == MathOperation.BOOL_INVERT:
            value = not bool(value)
        return value

    @classmethod
    def apply_scale(cls, value: float, input_min: float, input_max: float, output_min: float, output_max: float) \
            -> float or None:
        if value is None or input_min is None or input_max is None or output_min is None or output_max is None:
            return value
        value = ((value - input_min) * (output_max - output_min)) / (input_max - input_min) + output_min
        return value

    def publish_cov(self, point_store: PointStoreModel, device: DeviceModel = None, network: NetworkModel = None,
                    service_name: str = None):
        pass
