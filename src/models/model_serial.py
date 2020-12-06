from src import db
from src.interfaces.serial_network import ModbusRtuParity


class SerialDriverModel(db.Model):
    __tablename__ = 'serial'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=True, unique=False)
    port = db.Column(db.String(80), nullable=True, unique=False)
    speed = db.Column(db.Integer(), default=9600)
    stop_bits = db.Column(db.Integer(), default=1)
    parity = db.Column(db.Enum(ModbusRtuParity), default=ModbusRtuParity.N)
    byte_size = db.Column(db.Integer(), default=8)


    @classmethod
    def find_one(cls):
        return cls.query.first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def create_default_server_if_does_not_exist(cls):
        serial_driver = SerialDriverModel.find_one()
        if not serial_driver:
            # uuid_ = str(uuid.uuid4())
            # serial_driver = SerialDriverModel(uuid=uuid_,
            #                                   ip=device__ip,
            #                                   port=device__port,
            #                                   device_id=device__device_id,
            #                                   local_obj_name=device__local_obj_name,
            #                                   model_name=device__model_name,
            #                                   vendor_id=device__vendor_id,
            #                                   vendor_name=device__vendor_name)
            serial_driver.save_to_db()
        return serial_driver
