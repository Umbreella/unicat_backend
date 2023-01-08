import base64


def get_id_from_value(value):
    value_bytes = value.encode('ascii')
    value_decoded = base64.b64decode(value_bytes)
    value_str = value_decoded.decode('ascii')

    return value_str.split(':')[-1]


def get_value_from_model_id(model_name, model_id):
    value = f'{model_name}:{model_id}'

    value_bytes = value.encode('ascii')
    value_encoded = base64.b64encode(value_bytes)
    value_str = value_encoded.decode('ascii')

    return value_str
