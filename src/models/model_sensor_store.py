from src import db


class SensorStoreModel(db.Model):
    __tablename__ = 'sensors_store'

    sensor_uuid = db.Column(db.String, db.ForeignKey('sensors.uuid'), primary_key=True, nullable=False)
    pressure = db.Column(db.Float, nullable=True)
    temp = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    voltage = db.Column(db.Float, nullable=True)
    rssi = db.Column(db.Float, nullable=True)
    snr = db.Column(db.Float, nullable=True)
    lux = db.Column(db.Float, nullable=True)
    movement = db.Column(db.Integer, nullable=True)
    low_battery_alm = db.Column(db.Integer, nullable=True)
    micro_edge_pulse_count = db.Column(db.Float, nullable=True)
    micro_edge_A1 = db.Column(db.Float, nullable=True)
    micro_edge_A2 = db.Column(db.Float, nullable=True)
    micro_edge_A3 = db.Column(db.Float, nullable=True)
    ts = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f"PointStore(sensor_uuid = {self.sensor_uuid})"

    @classmethod
    def filter_by_sensor_uuid(cls, sensor_uuid):
        return cls.query.filter_by(sensor_uuid=sensor_uuid)

    @classmethod
    def create_new_point_store_model(cls, sensor_uuid):
        return SensorStoreModel(sensor_uuid=sensor_uuid)

    @classmethod
    def commit(cls):
        db.session.commit()
