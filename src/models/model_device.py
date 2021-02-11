import uuid

from sqlalchemy.orm import validates

from src import db
from src.interfaces.device import DeviceTypes, DeviceModels, verify_device_model
from src.models.model_base import ModelBase


class DeviceModel(ModelBase):
    __tablename__ = 'devices'

    name = db.Column(db.String(80), nullable=False, unique=True)
    device_id = db.Column(db.String(8), nullable=False, unique=True)
    enable = db.Column(db.Boolean, nullable=False, default=True)
    device_type = db.Column(db.Enum(DeviceTypes), nullable=False)
    device_model = db.Column(db.Enum(DeviceModels), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    fault = db.Column(db.Integer, nullable=True)
    points = db.relationship('PointModel', cascade="all,delete", backref='device', lazy=True)

    def __repr__(self):
        return "DeviceModel({})".format(self.uuid)

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, device_id: str):
        return cls.query.filter_by(device_id=device_id).first()

    def save_to_db(self):
        self.save_to_db_no_commit()
        super().save_to_db()

    def save_to_db_no_commit(self):
        if not self.points or not len(self.points):
            from src.models.device_point_presets import get_device_points
            device_points = get_device_points(self.device_model)
            for point in device_points:
                point.uuid = str(uuid.uuid4())
                point.device_point_name = point.name  # to match decoder key
                point.name = self.name + '_' + point.name
                point.device_uuid = self.uuid
                point.save_to_db_no_commit()
        super().save_to_db_no_commit()

    def delete_from_db(self):
        super().delete_from_db()

    @validates('device_model', 'device_type')
    def validate_device_model(self, key, value):
        if key == 'device_type':
            if isinstance(value, DeviceTypes):
                return value
            if not value or value not in DeviceTypes.__members__:
                raise ValueError("Invalid Device Type")
            value = DeviceTypes[value]
        else:
            if not isinstance(value, DeviceModels):
                if not value or value not in DeviceModels.__members__:
                    raise ValueError("Invalid Device Model")
                value = DeviceModels[value]

        # handle for both cases depending on which field is validated first
        if key == 'device_model' and self.device_type is not None:
            if not verify_device_model(self.device_type, value):
                raise ValueError('Invalid device model for device type')
        elif key == 'device_type' and self.device_model is not None:
            if not verify_device_model(value, self.device_model):
                raise ValueError('Invalid device model for device type')

        return value
