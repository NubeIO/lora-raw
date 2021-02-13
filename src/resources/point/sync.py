from flask_restful import Resource

from src.models.model_point_store import PointStoreModel


class LPGPSync(Resource):

    @classmethod
    def get(cls):
        PointStoreModel.sync_points_values(gp=True, bp=False)


class LPBPSync(Resource):

    @classmethod
    def get(cls):
        PointStoreModel.sync_points_values(gp=False, bp=True)
