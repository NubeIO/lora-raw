import uuid

from flask_restful import marshal_with

from src.models.model_device import DeviceModel
from src.resources.device.device_base import DeviceBase
from src.resources.mod_fields import device_fields


class DevicePlural(DeviceBase):
    @marshal_with(device_fields)
    def get(self):
        return DeviceModel.get_all()

    @marshal_with(device_fields)
    def post(self):
        uuid_ = str(uuid.uuid4())
        data = DevicePlural.parser.parse_args()
        return self.add_device(uuid_, data)
