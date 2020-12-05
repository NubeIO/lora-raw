from flask_restful import Api
from src import app
from src.platform.resource_wires_plat import WiresPlatResource
from src.system.resources.ping import Ping


api_prefix = 'api'
api = Api(app)

api.add_resource(Ping, "/{}/ping".format(api_prefix))


wires_api_prefix = f'{api_prefix}/wires'
api.add_resource(WiresPlatResource, f'/{wires_api_prefix}/plat')