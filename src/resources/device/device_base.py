from flask_restful import Resource, reqparse, abort

from src import db
from src.lora import DeviceRegistry
from src.models.model_device import DeviceModel


class DeviceBase(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('id', type=str, required=True, dest='device_id')
    parser.add_argument('enable', type=bool)
    parser.add_argument('device_type', type=str, required=True)
    parser.add_argument('device_model', type=str, required=True)
    parser.add_argument('description', type=str)

    def add_device(self, _uuid, data):
        try:
            device: DeviceModel = DeviceModel(uuid=_uuid, **data)
            device.save_to_db()
            DeviceRegistry().add_device(device.device_id, device.uuid)
            return device
        except Exception as e:
            abort(500, message=str(e))

    def update_device(self, _uuid, data):
        # TODO: patch all point names if name updated
        DeviceModel.filter_by_uuid(_uuid).update(data)
        db.session.commit()
        sensor_return = DeviceModel.find_by_uuid(_uuid)
        DeviceRegistry().add_device(sensor_return.name, _uuid)
        return sensor_return

    def delete_device(self, _uuid):
        device = DeviceModel.find_by_uuid(_uuid)
        if device:
            device.delete_from_db()
            DeviceRegistry().remove_device(device.device_id)
            return device
        return None
