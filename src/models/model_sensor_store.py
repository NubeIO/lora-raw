from sqlalchemy import and_, or_

from src import db


class SensorStore(db.Model):
    __tablename__ = 'sensors_store'
    point_uuid = db.Column(db.String, db.ForeignKey('sensors.uuid'), primary_key=True, nullable=False)
    present_value = db.Column(db.Float(), nullable=False)
    ts = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    pressure = db.Column(db.Float(), nullable=True)
    temp = db.Column(db.Float(), nullable=True)
    humidity = db.Column(db.Float(), nullable=True)
    voltage = db.Column(db.Float(), nullable=True)
    rssi = db.Column(db.Float(), nullable=True)
    snr = db.Column(db.Float(), nullable=True)
    lux = db.Column(db.Float(), nullable=True)
    movement = db.Column(db.Integer(), nullable=True)
    low_battery_alm = db.Column(db.Integer(), nullable=True)
    micro_edge_pulse_count = db.Column(db.Float(), nullable=True)
    micro_edge_A1 = db.Column(db.Float(), nullable=True)
    micro_edge_A2 = db.Column(db.Float(), nullable=True)
    micro_edge_A3 = db.Column(db.Float(), nullable=True)


    def __repr__(self):
        return f"PointStore(point_uuid = {self.point_uuid})"

    @classmethod
    def find_by_point_uuid(cls, point_uuid):
        return cls.query.filter_by(point_uuid=point_uuid).first()

    @classmethod
    def create_new_point_store_model(cls, point_uuid):
        return SensorStore(point_uuid=point_uuid, present_value=0)

    def update(self) -> bool:
        res = db.session.execute(self.__table__
                                 .update()
                                 .values(present_value=self.present_value)
                                 .where(and_(self.__table__.c.point_uuid == self.point_uuid,
                                             or_(self.__table__.c.present_value != self.present_value))))
        return bool(res.rowcount)
