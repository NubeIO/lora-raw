from src import db
from src.interfaces.sensor.sensor import EventState, SensorType, SensorModel, MicroEdgeInputType
from src.models.model_sensor_store import SensorStore


class SensorModel(db.Model):
    __tablename__ = 'sensors'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    object_name = db.Column(db.String(80), nullable=False, unique=True)
    address = db.Column(db.Integer(), nullable=False, unique=True)

    id = db.Column(db.String(120), nullable=False, unique=True)
    sensor_type = db.Column(db.Enum(SensorType), nullable=False)
    sensor_model = db.Column(db.Enum(SensorModel), nullable=False)
    micro_edge_input_type = db.Column(db.Enum(MicroEdgeInputType), nullable=False)
    sensor_wake_up_rate = db.Column(db.Integer(), nullable=False)

    description = db.Column(db.String(120), nullable=False)
    enable = db.Column(db.Boolean(), nullable=False)
    fault = db.Column(db.Integer(), nullable=True)
    data_round = db.Column(db.Integer(), nullable=True)
    data_offset = db.Column(db.Float(), nullable=True)
    point_store = db.relationship('SensorStore',
                                  backref='sensor',
                                  lazy=False,
                                  uselist=False,
                                  cascade="all,delete")
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f"SensorModel({self.uuid})"

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    @classmethod
    def filter_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid)

    @classmethod
    def find_by_object_id(cls, object_type, address):
        return cls.query.filter(
            (SensorModel.object_type == object_type) & (SensorModel.address == address)).first()

    @classmethod
    def find_by_object_name(cls, object_name):
        return cls.query.filter(SensorModel.object_name == object_name).first()

    @classmethod
    def delete_all_from_db(cls):
        cls.query.delete()
        db.session.commit()

    def save_to_db(self):
        # self.priority_array_write = PriorityArrayModel(sensor_uuid=self.uuid, **priority_array_write)
        print(2222)
        self.point_store = SensorStore.create_new_point_store_model(self.uuid)
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
