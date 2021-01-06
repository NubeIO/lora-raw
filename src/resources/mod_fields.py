from flask_restful import fields


point_store_fields = {
    'point_uuid': fields.String,
    'value': fields.Float,
    'value_original': fields.Float,
    'value_raw': fields.String,
    'fault': fields.Boolean,
    'fault_message': fields.String,
    'ts': fields.String
}

point_fields = {
    'uuid': fields.String,
    'name': fields.String,
    'device_point_name': fields.String,
    'device_uuid': fields.String,
    'enable': fields.Boolean,
    'cov_threshold': fields.Float,
    'value_round': fields.Float,
    'value_offset': fields.Float,
    'value_operation': fields.Float,
    'input_min': fields.Float,
    'input_max': fields.Float,
    'scale_min': fields.Float,
    'scale_max': fields.Float,
    'created_on': fields.String,
    'updated_on': fields.String,
    'point_store': fields.Nested(point_store_fields)
}

device_fields = {
    'uuid': fields.String,
    'name': fields.String,
    'id': fields.String(8, attribute='device_id'),
    'enable': fields.Boolean,
    'device_type': fields.String(attribute="device_type.name"),
    'device_model': fields.String(attribute="device_model.name"),
    'description': fields.String,
    'fault': fields.Integer,
    'created_on': fields.String,
    'updated_on': fields.String,
    'points': fields.Nested(point_fields)
}

network_fields = {
    'port': fields.String,
    'baud_rate': fields.Integer,
    'stop_bits': fields.Integer,
    'parity': fields.String(attribute="parity.name"),
    'byte_size': fields.Integer,
    'timeout': fields.Integer,
    'firmware_version': fields.String(attribute='firmware_version.name'),
    'encryption_key': fields.String
}
