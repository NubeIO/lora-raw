# from flask import current_app
from sqlalchemy import UniqueConstraint
# from sqlalchemy.orm import validates

from src import db
# from src.interfaces.point import HistoryType, MathOperation
from src.interfaces.point import MathOperation
from src.models.model_device import DeviceModel
from src.models.model_base import ModelBase
from src.models.model_network import NetworkModel
from src.models.model_point_store import PointStoreModel
# from src.models.model_point_store_history import PointStoreHistoryModel
# from src.services.event_service_base import Event, EventType
# from src.utils.model_utils import ModelUtils


class PointModel(ModelBase):
    __tablename__ = 'points'
    name = db.Column(db.String(80), nullable=False, unique=True)
    device_uuid = db.Column(db.String, db.ForeignKey('devices.uuid'), nullable=False)
    enable = db.Column(db.Boolean(), nullable=False, default=True)
    device_point_name = db.Column(db.String(), nullable=False)
    # history_enable = db.Column(db.Boolean(), nullable=False, default=False)
    # history_type = db.Column(db.Enum(HistoryType), nullable=False, default=HistoryType.INTERVAL)
    # history_interval = db.Column(db.Integer, nullable=False, default=15)
    # writable = db.Column(db.Boolean, nullable=False, default=False)
    # write_value = db.Column(db.Float, nullable=True, default=None)  # TODO: more data types...
    cov_threshold = db.Column(db.Float, nullable=False, default=0)
    value_round = db.Column(db.Integer(), nullable=False, default=2)
    value_offset = db.Column(db.Float(), nullable=False, default=0)
    value_operation = db.Column(db.Enum(MathOperation), nullable=True)
    input_min = db.Column(db.Float())
    input_max = db.Column(db.Float())
    scale_min = db.Column(db.Float())
    scale_max = db.Column(db.Float())
    point_store = db.relationship('PointStoreModel', backref='point', lazy=False, uselist=False, cascade="all,delete")
    # point_store_history = db.relationship('PointStoreHistoryModel', backref='point')
    # driver = db.Column(db.String(80))

    __table_args__ = (
        UniqueConstraint('name', 'device_uuid'),
    )

    def __repr__(self):
        return f"Point(uuid = {self.uuid})"

    @classmethod
    def find_by_name(cls, point_name: str, device_name: str, network_name: str):
        results = cls.query.filter_by(name=point_name) \
            .join(DeviceModel).filter_by(name=device_name) \
            .join(NetworkModel).filter_by(name=network_name) \
            .first()
        return results

    @classmethod
    def filter_by_uuid(cls, uuid: str):
        return cls.query.filter_by(uuid=uuid)

    @classmethod
    def find_by_uuid(cls, uuid: str):
        return cls.query.filter_by(uuid=uuid).first()

    def save_to_db(self):
        self.point_store = PointStoreModel.create_new_point_store_model(self.uuid)
        super().save_to_db()

    def save_to_db_no_commit(self):
        self.point_store = PointStoreModel.create_new_point_store_model(self.uuid)
        super().save_to_db_no_commit()

    def update_point_value(self, point_store: PointStoreModel, cov_threshold: float = None) -> bool:
        if not point_store.fault:
            if cov_threshold is None:
                cov_threshold = self.cov_threshold

            value = point_store.value_original
            if value is not None:
                value = self.apply_scale(value, self.input_min, self.input_max, self.scale_min,
                                         self.scale_max)
                value = self.apply_offset(value, self.value_offset, self.value_operation)
                value = round(value, self.value_round)
            point_store.value = value
        return point_store.update(cov_threshold)

    # @validates('history_interval')
    # def validate_history_interval(self, _, value):
    #     if self.history_type == HistoryType.INTERVAL and value is not None and value < 1:
    #         raise ValueError("history_interval needs to be at least 1, default is 15 (in minutes)")
    #     return value

    # def get_model_event_name(self) -> str:
    #     return 'point'
    #
    # def get_model_event_type(self) -> EventType:
    #     return EventType.POINT_UPDATE

    # def update(self, **kwargs):
    #     super().update(**kwargs)
    #
    #     point_store: PointStoreModel = PointStoreModel.find_by_point_uuid(self.uuid)
    #     updated = point_store.update(0)
    #     self.point_store = point_store
    #     if updated:
    #         self.publish_cov(self.point_store)
    #
    #     return self

    @classmethod
    def apply_offset(cls, original_value: float, value_offset: float, value_operation: MathOperation) -> float or None:
        """Do calculations on original value with the help of point details"""
        if original_value is None or value_operation is None:
            return original_value
        value = original_value
        if value_operation == MathOperation.ADD:
            value += value_offset
        elif value_operation == MathOperation.SUBTRACT:
            value -= value_offset
        elif value_operation == MathOperation.MULTIPLY:
            value *= value_offset
        elif value_operation == MathOperation.DIVIDE:
            value /= value_offset
        elif value_operation == MathOperation.BOOL_INVERT:
            value = not bool(value)
        return value

    @classmethod
    def apply_scale(cls, value: float, input_min: float, input_max: float, output_min: float, output_max: float) \
            -> float or None:
        if value is None or input_min is None or input_max is None or output_min is None or output_max is None:
            return value
        value = ((value - input_min) * (output_max - output_min)) / (input_max - input_min) + output_min
        return value

    def publish_cov(self, point_store: PointStoreModel, device: DeviceModel = None, network: NetworkModel = None,
                    service_name: str = None):
        pass
        # if point_store is None:
        #     raise Exception('Point.publish_cov point_store cannot be None')
        # if device is None:
        #     device = DeviceModel.find_by_uuid(self.device_uuid)
        # if network is None:
        #     network = NetworkModel.find_by_uuid(device.network_uuid)
        # if device is None or network is None:
        #     raise Exception(f'Cannot find network or device for point {self.uuid}')
        # if service_name is None:
        #     service_name = network.driver
        #
        # if self.history_enable and self.history_type == HistoryType.COV and network.history_enable and \
        #     device.history_enable:
        #     self.create_history(point_store)
        #
        # from src import EventDispatcher
        # EventDispatcher().dispatch_from_source(None, Event(EventType.POINT_COV, {
        #     'point': self,
        #     'point_store': point_store,
        #     'device': device,
        #     'network': network,
        #     'source_driver': service_name
        # }))

    # def create_history(self, point_store: PointStoreModel):
    #     from src import AppSetting
    #     setting: AppSetting = current_app.config[AppSetting.KEY]
    #     if setting.services.histories:
    #         data = ModelUtils.row2dict_default(point_store)
    #         _point_store_history = PointStoreHistoryModel(**data)
    #         _point_store_history.save_to_db_no_commit()
