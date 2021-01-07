from flask import Blueprint
from flask_restful import Api

from src.resources.ping import Ping
from src.resources.device.device_plural import DevicePlural
from src.resources.device.device_singular import DeviceSingular
from src.resources.network.network import SerialDriver

bp_lora = Blueprint('lora', __name__, url_prefix='/api/lora')
apiLora = Api(bp_lora)
apiLora.add_resource(SerialDriver, '/networks')
apiLora.add_resource(DevicePlural, '/devices')
apiLora.add_resource(DeviceSingular, '/devices/<string:key>/<string:name_or_uuid>')
# /devices/uuid/<string:uuid>
# /devices/name/<string:name>

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
Api(bp_system).add_resource(Ping, '', '/ping')
