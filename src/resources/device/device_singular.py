from flask_restful import abort, marshal_with, reqparse

from src.models.model_device import DeviceModel
from src.resources.mod_fields import device_fields
from src.resources.device.device_base import DeviceBase


class DeviceSingular(DeviceBase):
    parser_patch = reqparse.RequestParser()
    parser_patch.add_argument('name', type=str)
    parser_patch.add_argument('device_type', type=str)
    parser_patch.add_argument('device_model', type=str)
    parser_patch.add_argument('description', type=str)
    parser_patch.add_argument('enable', type=bool)

    @marshal_with(device_fields)
    def get(self, uuid):
        sensor = DeviceModel.find_by_uuid(uuid)
        if not sensor:
            abort(404, message='LoRa Sensor is not found')
        return sensor

    @marshal_with(device_fields)
    def patch(self, _uuid):
        data = DeviceSingular.parser_patch.parse_args()
        sensor = DeviceModel.find_by_uuid(_uuid)
        if sensor is None:
            abort(404, message="Does not exist {}".format(_uuid))
        try:
            non_none_data = {}
            for key in data.keys():
                if data[key] is not None:
                    non_none_data[key] = data[key]
            return self.update_device(_uuid, non_none_data)
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
