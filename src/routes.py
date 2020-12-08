from flask_restful import Api

from src import app
from src.resources.ping import Ping
from src.resources.sensor.sensor_name import SensorName
from src.resources.sensor.sensor_plural import SensorPlural
from src.resources.sensor.sensor_singular import SensorSingular
from src.resources.serial_driver.serial import SerialDriver

api_prefix = 'api'
api = Api(app)

api.add_resource(SerialDriver, '/{}/lora/port'.format(api_prefix))
api.add_resource(SensorPlural, '/{}/lora/sensors'.format(api_prefix))
api.add_resource(SensorSingular, '/{}/lora/sensors/uuid/<string:uuid>'.format(api_prefix))
api.add_resource(SensorName, '/{}/lora/sensors/name/<string:object_name>'.format(api_prefix))
api.add_resource(Ping, '/{}/system/ping'.format(api_prefix))
