from datetime import datetime

import jwt
from django.contrib.auth import get_user_model
from django.utils import timezone
from graphql_jwt.compat import get_operation_name
from graphql_jwt.settings import jwt_settings


def get_timeout_seconds(time_end: datetime) -> int:
    if time_end is None:
        return None

    timeout = time_end - timezone.now()
    timeout_total_seconds = timeout.total_seconds()

    return int(timeout_total_seconds)


def allow_any(info, **kwargs):
    try:
        operation_name = get_operation_name(info.operation.operation).title()
        operation_type = info.schema.get_type(operation_name)

        if hasattr(operation_type, 'fields'):

            field = operation_type.fields.get(info.field_name)

            if field is None:
                return False

        else:
            return False

        graphene_type = getattr(field.type, 'graphene_type', None)

        return graphene_type is not None and issubclass(
            graphene_type, tuple(jwt_settings.JWT_ALLOW_ANY_CLASSES)
        )
    except Exception:
        return False


def jwt_decode(token, context=None):
    from django.conf import settings

    SIMPLE_JWT = settings.SIMPLE_JWT

    return jwt.decode(
        token,
        SIMPLE_JWT['SIGNING_KEY'],
        options={
            'verify_exp': jwt_settings.JWT_VERIFY_EXPIRATION,
            'verify_aud': jwt_settings.JWT_AUDIENCE is not None,
            'verify_signature': jwt_settings.JWT_VERIFY,
        },
        audience=SIMPLE_JWT['AUDIENCE'],
        issuer=SIMPLE_JWT['ISSUER'],
        leeway=SIMPLE_JWT['LEEWAY'],
        algorithms=[SIMPLE_JWT['ALGORITHM']],
    )


def get_username_by_payload(payload):
    return payload.get('user_id', None)


def get_user_by_natural_key(user_id):
    UserModel = get_user_model()
    try:
        return UserModel.objects.get(pk=user_id)
    except UserModel.DoesNotExist:
        return None
