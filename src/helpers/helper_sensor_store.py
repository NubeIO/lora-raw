from src import db
from src.models.model_sensor_store import SensorStore


def update_sensor_store(sensor_uuid, present_value):
    point_store = SensorStore(sensor_uuid=sensor_uuid, present_value=present_value)
    point_store.update()
    db.session.commit()
