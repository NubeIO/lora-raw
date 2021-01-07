from flask_restful import abort, marshal_with, reqparse

from src.models.model_device import DeviceModel
from src.resources.mod_fields import device_fields
from src.resources.device.device_base import DeviceBase


class DeviceSingular(DeviceBase):
    parser_patch = reqparse.RequestParser()
    parser_patch.add_argument('name', type=str, store_missing=False)
    parser_patch.add_argument('id', type=str, dest='device_id', store_missing=False)
    parser_patch.add_argument('device_type', type=str, store_missing=False)
    parser_patch.add_argument('device_model', type=str, store_missing=False)
    parser_patch.add_argument('description', type=str, store_missing=False)
    parser_patch.add_argument('enable', type=bool, store_missing=False)

    @marshal_with(device_fields)
    def get(self, key, name_or_uuid):
        device = self.__get_device(key, name_or_uuid)
        if not device:
            abort(404, message='LoRa Sensor is not found')
        return device

    @marshal_with(device_fields)
    def patch(self, key, name_or_uuid):
        data = DeviceSingular.parser_patch.parse_args()
        device = self.__get_device(key, name_or_uuid)
        if device is None:
            abort(404, message="Does not exist {}".format(name_or_uuid))
        try:
            return self.update_device(device, data)
        except Exception as e:
            abort(500, message=str(e))

    def delete(self, _uuid):
        device = self.delete_device(_uuid)
        if device:
            return '', 204
        elif device is None:
            return 'No device found', 404
        else:
            abort(500, message='unknown delete device error')

    def __get_device(self, key, name_or_uuid):
        if key == 'uuid':
            return DeviceModel.find_by_uuid(name_or_uuid)
        if key == 'name':
            return DeviceModel.find_by_name(name_or_uuid)
