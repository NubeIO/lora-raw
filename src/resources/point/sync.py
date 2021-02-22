from rubix_http.resource import RubixResource

from src.models.model_point_store import PointStoreModel


class LPGPSync(RubixResource):

    @classmethod
    def get(cls):
        PointStoreModel.sync_points_values(gp=True, bp=False)


class LPBPSync(RubixResource):

    @classmethod
    def get(cls):
        PointStoreModel.sync_points_values(gp=False, bp=True)
