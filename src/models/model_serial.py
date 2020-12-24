import uuid

from src.app import db, SerialSetting
from src.interfaces.serial_network import ModbusRtuParity
from src.models.model_base import ModelBase


class SerialDriverModel(ModelBase):
    __tablename__ = 'serial'

    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=True, unique=False)
    port = db.Column(db.String(80), nullable=True, unique=False)
    baud_rate = db.Column(db.Integer, default=9600)
    stop_bits = db.Column(db.Integer, default=1)
    parity = db.Column(db.Enum(ModbusRtuParity), default=ModbusRtuParity.N)
    byte_size = db.Column(db.Integer, default=8)
    timeout = db.Column(db.Integer, default=5)

    @classmethod
    def filter_one(cls):
        return cls.query.filter()

    @classmethod
    def find_one(cls):
        return cls.query.first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def create_default_server_if_does_not_exist(cls, config: SerialSetting):
        serial_driver = SerialDriverModel.find_one()
        if not serial_driver:
            uuid_ = str(uuid.uuid4())
            serial_driver = SerialDriverModel(uuid=uuid_,
                                              name=config.name,
                                              port=config.port,
                                              baud_rate=config.baud_rate,
                                              stop_bits=config.stop_bits,
                                              parity=config.parity,
                                              byte_size=config.byte_size,
                                              timeout=config.timeout)
            serial_driver.save_to_db()
        return serial_driver
