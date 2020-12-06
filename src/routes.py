from flask_restful import Api

from src import app
from src.resources.ping import Ping
from src.resources.sensor.sensor_name import SensorName
from src.resources.sensor.sensor_plural import SensorPlural
from src.resources.sensor.sensor_singular import SensorSingular
from src.resources.serial_driver.serial import SerialDriver

api_prefix = 'api'
api = Api(app)

api.add_resource(SerialDriver, f'/{api_prefix}/lora/port')
api.add_resource(SensorPlural, f'/{api_prefix}/lora/sensors')
api.add_resource(SensorSingular, f'/{api_prefix}/lora/sensors/uuid/<string:uuid>')
api.add_resource(SensorName, f'/{api_prefix}/lora/sensors/name/<string:object_name>')
api.add_resource(Ping, f'/{api_prefix}/system/ping')
