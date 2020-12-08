from src import db
from src.interfaces.sensor.sensor import SensorType, SensorModelType, MicroEdgeInputType
from src.lora.droplet_registry import DropletsRegistry
from src.models.model_base import ModelBase
from src.models.model_sensor_store import SensorStoreModel


class SensorModel(ModelBase):
    __tablename__ = 'sensors'

    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    object_name = db.Column(db.String(80), nullable=False, unique=True)
    address = db.Column(db.Integer, nullable=False, unique=True)

    sensor_type = db.Column(db.Enum(SensorType), nullable=False)
    sensor_model = db.Column(db.Enum(SensorModelType), nullable=False)
    micro_edge_input_type = db.Column(db.Enum(MicroEdgeInputType), nullable=False)
    sensor_wake_up_rate = db.Column(db.Integer, nullable=False)

    description = db.Column(db.String(120), nullable=False)
    enable = db.Column(db.Boolean, nullable=False)
    fault = db.Column(db.Integer, nullable=True)
    data_round = db.Column(db.Integer, default=2)
    data_offset = db.Column(db.Float, default=0)
    sensor_store = db.relationship('SensorStoreModel',
                                   backref='sensor',
                                   lazy=False,
                                   uselist=False,
                                   cascade="all,delete")
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        # return f"SensorModel({self.uuid})"
        return "SensorModel({})".format(self.uuid)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    @classmethod
    def filter_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid)

    @classmethod
    def find_by_object_id(cls, object_type, address):
        return cls.query.filter((SensorModel.object_type == object_type) & (SensorModel.address == address)).first()

    @classmethod
    def find_by_object_name(cls, object_name):
        return cls.query.filter(SensorModel.object_name == object_name).first()

    @classmethod
    def delete_all_from_db(cls):
        cls.query.delete()
        db.session.commit()
        DropletsRegistry.get_instance().remove_all_droplets()

    def save_to_db(self):
        self.sensor_store = SensorStoreModel.create_new_sensor_store_model(self.uuid)
        db.session.add(self)
        db.session.commit()
        DropletsRegistry.get_instance().add_droplet(self.object_name, self.uuid)

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        DropletsRegistry.get_instance().remove_droplet(self.object_name)
