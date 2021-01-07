import uuid
from sqlalchemy.orm import validates

from src import db, SerialSetting
from src.interfaces.network import SerialParity, SupportedFirmwareVersion
from src.models.model_base import ModelBase


class NetworkModel(ModelBase):
    __tablename__ = 'network'

    name = db.Column(db.String(80), nullable=False)
    port = db.Column(db.String(40), nullable=False, unique=True)
    baud_rate = db.Column(db.Integer, default=9600)
    stop_bits = db.Column(db.Integer, default=1)
    parity = db.Column(db.Enum(SerialParity), default=SerialParity.N)
    byte_size = db.Column(db.Integer, default=8)
    timeout = db.Column(db.Integer, default=5)
    firmware_version = db.Column(db.Enum(SupportedFirmwareVersion), nullable=False)
    encryption_key = db.Column(db.String(32))

    @classmethod
    def filter_one(cls):
        return cls.query.filter()

    @classmethod
    def find_one(cls):
        driver = cls.query.first()
        if driver:
            db.session.refresh(driver)
        return driver

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def create_network(cls, config: SerialSetting):
        serial_driver = NetworkModel.find_one()
        if not serial_driver:
            uuid_ = str(uuid.uuid4())
            serial_driver = NetworkModel(uuid=uuid_,
                                         name=config.port,
                                         port=config.port,
                                         baud_rate=config.baud_rate,
                                         stop_bits=config.stop_bits,
                                         parity=config.parity,
                                         byte_size=config.byte_size,
                                         timeout=config.timeout,
                                         firmware_version=config.firmware_version,
                                         encryption_key=config.encryption_key)
            serial_driver.save_to_db()
        else:
            db.session.refresh(serial_driver)

        return serial_driver

    @validates('port')
    def validate_name(self, _, value):
        self.name = value
        return value

    @validates('firmware_version')
    def validate_data_endian(self, _, value):
        if isinstance(value, SupportedFirmwareVersion):
            return value
        if not value or value not in SupportedFirmwareVersion.__members__:
            raise ValueError("Invalid Firmware Version")
        return SupportedFirmwareVersion[value]

    @validates('encryption_key')
    def validate_encryption_key(self, _, value):
        # TODO: handle self.firmware_version is None when this is validated first
        if self.firmware_version == SupportedFirmwareVersion.v1 or \
                self.firmware_version == SupportedFirmwareVersion.v2_encryption:
            return None
        else:
            assert len(value) == 32
            return value
