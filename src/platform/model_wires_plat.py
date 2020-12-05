from src import db
from src.platform.model_base import ModelBase


class WiresPlatModel(ModelBase):
    __tablename__ = 'wires_plat'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    device_id = db.Column(db.String(80), nullable=False)
    device_name = db.Column(db.String(80), nullable=False)
    client_id = db.Column(db.String(80), nullable=False)
    client_name = db.Column(db.String(80), nullable=False)
    site_id = db.Column(db.String(80), nullable=False)
    site_name = db.Column(db.String(80), nullable=False)
    site_address = db.Column(db.String(80), nullable=False)
    site_city = db.Column(db.String(80), nullable=False)
    site_state = db.Column(db.String(80), nullable=False)
    site_zip = db.Column(db.String(80), nullable=False)
    site_country = db.Column(db.String(80), nullable=False)
    site_lat = db.Column(db.String(80), nullable=False)
    site_lon = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"Wires({self.uuid})"

    @classmethod
    def find_one(cls):
        return cls.query.first()

    @classmethod
    def find_by_uuid(cls, wires_uuid):
        return cls.query.filter_by(uuid=wires_uuid).first()

    @classmethod
    def filter_by_uuid(cls, wires_uuid):
        return cls.query.filter_by(uuid=wires_uuid)

    @classmethod
    def delete_from_db(cls):
        cls.query.delete()
        db.session.commit()
