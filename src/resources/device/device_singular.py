from abc import abstractmethod

from flask_restful import abort, marshal_with, reqparse

from src.models.model_device import DeviceModel
from src.resources.device.device_base import DeviceBase
from src.resources.model_fields import device_fields


class DeviceSingularBase(DeviceBase):
    parser_patch = reqparse.RequestParser()
    parser_patch.add_argument('name', type=str, store_missing=False)
    parser_patch.add_argument('id', type=str, dest='device_id', store_missing=False)
    parser_patch.add_argument('device_type', type=str, store_missing=False)
    parser_patch.add_argument('device_model', type=str, store_missing=False)
    parser_patch.add_argument('description', type=str, store_missing=False)
    parser_patch.add_argument('enable', type=bool, store_missing=False)

    @classmethod
    @marshal_with(device_fields)
    def get(cls, value):
        device = cls.get_device(value)
        if not device:
            abort(404, message='LoRa Device is not found')
        return device

    @classmethod
    @marshal_with(device_fields)
    def patch(cls, value):
        data = DeviceSingularBase.parser_patch.parse_args()
        device = cls.get_device(value)
        if device is None:
            abort(404, message="Does not exist {}".format(value))
        try:
            return cls.update_device(device, data)
        except Exception as e:
            abort(500, message=str(e))

    @classmethod
    def delete(cls, value):
        device = cls.get_device(value)
        cls.delete_device(device)
        return '', 204

    @classmethod
    @abstractmethod
    def get_device(cls, value) -> DeviceModel:
        raise NotImplementedError('Need to implement')


class DeviceSingularByUUID(DeviceSingularBase):
    @classmethod
    def get_device(cls, value) -> DeviceModel:
        return DeviceModel.find_by_uuid(value)


class DeviceSingularByName(DeviceSingularBase):
    @classmethod
    def get_device(cls, value) -> DeviceModel:
        return DeviceModel.find_by_name(value)
