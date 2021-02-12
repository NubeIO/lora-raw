from flask import Blueprint
from flask_restful import Api

from src.resources.device.device_plural import DevicePlural
from src.resources.device.device_singular import DeviceSingularByName, DeviceSingularByUUID
from src.resources.mapping.mapping import LPGBPMappingResourceList, LPGBPMappingResourceByLoRaPointUUID, \
    LPGBPMappingResourceByGenericPointUUID, LPGBPMappingResourceByBACnetPointUUID
from src.resources.network.network import SerialDriver
from src.resources.ping import Ping
from src.resources.point.point import PointsSingularByName, PointsSingularByUUID, PointsPlural

bp_lora = Blueprint('lora', __name__, url_prefix='/api/lora')
api_lora = Api(bp_lora)
api_lora.add_resource(SerialDriver, '/networks')
api_lora.add_resource(DevicePlural, '/devices')
api_lora.add_resource(PointsPlural, '/points')
api_lora.add_resource(DeviceSingularByUUID, '/devices/uuid/<string:value>')
api_lora.add_resource(DeviceSingularByName, '/devices/name/<string:value>')
api_lora.add_resource(PointsSingularByUUID, '/points/uuid/<string:value>')
api_lora.add_resource(PointsSingularByName, '/points/name/<string:value>')

# lora to generic/bacnet points mappings
bp_lp_gbp_mapping = Blueprint('lp_gbp_mappings', __name__, url_prefix='/api/lp_gbp/mappings')
api_lp_gbp_mapping = Api(bp_lp_gbp_mapping)
api_lp_gbp_mapping.add_resource(LPGBPMappingResourceList, '')
api_lp_gbp_mapping.add_resource(LPGBPMappingResourceByLoRaPointUUID, '/lora/<string:point_uuid>')
api_lp_gbp_mapping.add_resource(LPGBPMappingResourceByGenericPointUUID, '/generic/<string:point_uuid>')
api_lp_gbp_mapping.add_resource(LPGBPMappingResourceByBACnetPointUUID, '/bacnet/<string:point_uuid>')

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
Api(bp_system).add_resource(Ping, '/ping')
