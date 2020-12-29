from flask import Blueprint
from flask_restful import Api

from src.resources.ping import Ping
from src.resources.sensor.sensor_name import SensorName
from src.resources.sensor.sensor_plural import SensorPlural
from src.resources.sensor.sensor_singular import SensorSingular
from src.resources.serial_driver.serial import SerialDriver

bp_lora = Blueprint('lora', __name__, url_prefix='/api/lora')
apiLora = Api(bp_lora)
apiLora.add_resource(SerialDriver, '/networks')
apiLora.add_resource(SensorPlural, '/devices')
apiLora.add_resource(SensorSingular, '/devices/uuid/<string:uuid>')
apiLora.add_resource(SensorName, '/devices/name/<string:name>')

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
Api(bp_system).add_resource(Ping, '/ping')
