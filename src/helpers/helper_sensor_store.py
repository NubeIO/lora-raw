from src import db
from src.models.model_sensor_store import SensorStore


def update_point_store(point_uuid, present_value):
    point_store = SensorStore(point_uuid=point_uuid, present_value=present_value)
    point_store.update()
    db.session.commit()
