from flask import Blueprint
from flask_restful import Api

from src.resources.device.device_plural import DevicePlural
from src.resources.device.device_singular import DeviceSingularByName, DeviceSingularByUUID
from src.resources.network.network import SerialDriver
from src.resources.ping import Ping

bp_lora = Blueprint('lora', __name__, url_prefix='/api/lora')
api_lora = Api(bp_lora)
api_lora.add_resource(SerialDriver, '/networks')
api_lora.add_resource(DevicePlural, '/devices')
api_lora.add_resource(DeviceSingularByUUID, '/devices/uuid/<string:value>')
api_lora.add_resource(DeviceSingularByName, '/devices/name/<string:value>')

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
Api(bp_system).add_resource(Ping, '/ping')
