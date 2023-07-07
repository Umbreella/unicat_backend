from rest_framework.permissions import DjangoModelPermissions


class DjModelPermForDRF(DjangoModelPermissions):
    perms_map = {
        **DjangoModelPermissions.perms_map,
        'GET': ['%(app_label)s.view_%(model_name)s'],
    }
