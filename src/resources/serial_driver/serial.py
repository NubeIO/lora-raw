import copy

from flask_restful import reqparse, marshal_with, Resource, abort

from src import db
# from src.bac_server import BACServer
from src.models.model_server import BACnetServerModel
from src.resources.mod_fields import server_field


class BACnetServer(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('ip', type=str)
    parser.add_argument('port', type=int)
    parser.add_argument('device_id', type=str)
    parser.add_argument('local_obj_name', type=str)
    parser.add_argument('model_name', type=str)
    parser.add_argument('vendor_id', type=str)
    parser.add_argument('vendor_name', type=str)

    @marshal_with(server_field)
    def get(self):
        return BACnetServerModel.find_one()

    @marshal_with(server_field)
    def patch(self):
        data = BACnetServer.parser.parse_args()
        data_to_update = {}
        old_bacnet_server = copy.deepcopy(BACnetServerModel.find_one())
        for key in data.keys():
            if data[key] is not None:
                data_to_update[key] = data[key]
        BACnetServerModel.query.filter().update(data_to_update)
        new_bacnet_server = BACnetServerModel.find_one()
        try:
            # BACServer.get_instance().restart_bac(old_bacnet_server, new_bacnet_server)
            db.session.commit()
            return new_bacnet_server
        except Exception as e:
            db.session.rollback()
            abort(501, message=str(e))
