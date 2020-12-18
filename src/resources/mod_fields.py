from flask_restful import fields

sensor_store_fields = {
    'pressure': fields.Float,
    'temp': fields.Float,
    'humidity': fields.Float,
    'voltage': fields.Float,
    'rssi': fields.Float,
    'snr': fields.Float,
    'lux': fields.Float,
    'movement': fields.Float,
    'low_battery_alm': fields.Integer,
    'micro_edge_pulse_count': fields.Integer,
    'micro_edge_A1': fields.Float,
    'micro_edge_A2': fields.Float,
    'micro_edge_A3': fields.Float,
    'ts': fields.String
}

sensor_fields = {
    'uuid': fields.String,
    'name': fields.String,
    'id': fields.String(8, attribute='device_id'),

    'sensor_type': fields.String(attribute="sensor_type.name"),
    'sensor_model': fields.String(attribute="sensor_model.name"),
    'micro_edge_input_type': fields.String(attribute="micro_edge_input_type.name"),
    'sensor_wake_up_rate': fields.Integer,

    'description': fields.String,
    'enable': fields.Boolean,
    'fault': fields.Integer,
    'data_round': fields.Integer,
    'data_offset': fields.Float,
    'created_on': fields.String,
    'updated_on': fields.String,
    'sensor_store': fields.Nested(sensor_store_fields)
}

serial_driver_field = {
    'uuid': fields.String,
    'name': fields.String,
    'port': fields.String,
    'baud_rate': fields.Integer,
    'stop_bits': fields.Integer,
    'parity': fields.String(attribute="parity.name"),
    'byte_size': fields.Integer,
    'timeout': fields.Integer,
}
