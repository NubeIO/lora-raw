from flask_restful import Api

from src import app
from src.resources.ping import Ping
from src.resources.sensor.sensor_name import SensorName
from src.resources.sensor.sensor_plural import SensorPlural
from src.resources.sensor.sensor_singular import SensorSingular
from src.resources.serial_driver.serial import SerialDriver

api_prefix = '/api'
api = Api(app)

lora_api_prefix = '{}/lora'.format(api_prefix)
api.add_resource(SerialDriver, '{}/networks'.format(lora_api_prefix))
api.add_resource(SensorPlural, '{}/devices'.format(lora_api_prefix))
api.add_resource(SensorSingular, '{}/devices/uuid/<string:uuid>'.format(lora_api_prefix))
api.add_resource(SensorName, '{}/devices/name/<string:name>'.format(lora_api_prefix))

system_api_prefix = '{}/system'.format(api_prefix)
api.add_resource(Ping, system_api_prefix, '{}/ping'.format(system_api_prefix))
