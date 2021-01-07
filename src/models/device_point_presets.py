from .model_point import PointModel
from src.interfaces.device import DeviceModels


# NOTE: names must match decoder payload names/keys


MICRO_EDGE_POINTS = [
    {'name': 'voltage',
     'cov_threshold': 0.01},
    {'name': 'rssi',
     'cov_threshold': 1},
    {'name': 'snr',
     'cov_threshold': 1},
    {'name': 'pulses',
     'cov_threshold': 1},
    {'name': 'AI1'},
    {'name': 'AI2'},
    {'name': 'AI3'},
    {'name': 'AI1_config'},
    {'name': 'AI2_config'},
    {'name': 'AI3_config'},
]

DROPLET_TH_POINTS = [
    {'name': 'voltage',
     'cov_threshold': 0.01},
    {'name': 'rssi',
     'cov_threshold': 1},
    {'name': 'snr',
     'cov_threshold': 1},
    {'name': 'temperature',
     'cov_threshold': 0.01},
    {'name': 'humidity',
     'cov_threshold': 1},
    {'name': 'pressure',
     'cov_threshold': 1},
]

DROPLET_THL_POINTS = DROPLET_TH_POINTS.copy()
DROPLET_THL_POINTS.extend([
    {'name': 'light',
     'cov_threshold': 1},
])

DROPLET_THLM_POINTS = DROPLET_THL_POINTS.copy()
DROPLET_THLM_POINTS.extend([
    {'name': 'motion',
     'cov_threshold': 1},
])

__DROPLET_THA_POINTS = [
    {'name': 'airflow',
     'cov_threshold': 0.01},
    {'name': 'duct_temperature',
     'cov_threshold': 0.01},
    {'name': 'duct_humidity',
     'cov_threshold': 1},
]
DROPLET_THA_POINTS = DROPLET_TH_POINTS.copy()
DROPLET_THA_POINTS.extend(__DROPLET_THA_POINTS)

DROPLET_THLA_POINTS = DROPLET_THL_POINTS.copy()
DROPLET_THLA_POINTS.extend(__DROPLET_THA_POINTS)


def get_device_points(model: DeviceModels):
    if model is DeviceModels.MICRO_EDGE:
        points_json = MICRO_EDGE_POINTS
    elif model is DeviceModels.DROPLET_TH:
        points_json = DROPLET_TH_POINTS
    elif model is DeviceModels.DROPLET_THL:
        points_json = DROPLET_THL_POINTS
    elif model is DeviceModels.DROPLET_THLM:
        points_json = DROPLET_THLM_POINTS
    elif model is DeviceModels.DROPLET_THA:
        points_json = DROPLET_THA_POINTS
    elif model is DeviceModels.DROPLET_THLA:
        points_json = DROPLET_THLA_POINTS
    else:
        raise Exception('Invalid DeviceModel')
    point_models = []
    for data in points_json:
        point_models.append(PointModel(**data))
    return point_models
