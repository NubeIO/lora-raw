from flask_restful import Resource, reqparse, abort
from sqlalchemy.exc import IntegrityError

from src import db
from src.lora import DeviceRegistry
from src.models.model_device import DeviceModel


class DeviceBase(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, store_missing=False)
    parser.add_argument('id', type=str, required=True, dest='device_id', store_missing=False)
    parser.add_argument('enable', type=bool, store_missing=False)
    parser.add_argument('device_type', type=str, required=True, store_missing=False)
    parser.add_argument('device_model', type=str, required=True, store_missing=False)
    parser.add_argument('description', type=str, store_missing=False)

    @classmethod
    def add_device(cls, _uuid: str, data: dict):
        try:
            device: DeviceModel = DeviceModel(uuid=_uuid, **data)
            device.save_to_db()
            DeviceRegistry().add_device(device.device_id, device.uuid)
            return device
        except IntegrityError as e:
            abort(400, message=str(e.orig))
        except Exception as e:
            abort(500, message=str(e))

    @classmethod
    def update_device(cls, device: DeviceModel, data: dict):
        original_device_id = device.device_id
        original_device_name = device.name
        DeviceModel.filter_by_uuid(device.uuid).update(data)
        if original_device_id != device.device_id:
            DeviceRegistry().remove_device(original_device_id)
        if original_device_name != device.name:
            for point in device.points:
                point.name = point.name.replace(original_device_name, device.name)
        db.session.commit()
        DeviceRegistry().add_device(device.device_id, device.uuid)
        return device

    @classmethod
    def delete_device(cls, device):
        if not device:
            abort(404, message=f'Device not found')
        device.delete_from_db()
        DeviceRegistry().remove_device(device.device_id)
