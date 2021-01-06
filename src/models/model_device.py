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
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def filter_by_uuid(cls, uuid: str):
        return cls.query.filter_by(uuid=uuid)

    @classmethod
    def find_by_uuid(cls, uuid: str):
        return cls.query.filter_by(uuid=uuid).first()

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
        super().save_to_db_no_commit()

    def delete_from_db(self):
        super().delete_from_db()

    @classmethod
    def delete_all_from_db(cls):
        cls.query.delete()
        db.session.commit()

    @validates('device_type')
    def validate_device_type(self, _, value):
        if isinstance(value, DeviceTypes):
            return value
        if not value or value not in DeviceTypes.__members__:
            raise ValueError("Invalid Device Type")
        return DeviceTypes[value]

    @validates('device_model')
    def validate_device_model(self, _, value):
        if not isinstance(value, DeviceModels):
            if not value or value not in DeviceModels.__members__:
                raise ValueError("Invalid Firmware Version")
            value = DeviceModels[value]
        if not verify_device_model(self.device_type, self.device_model):
            raise ValueError('Invalid device model for device type')
        return value



