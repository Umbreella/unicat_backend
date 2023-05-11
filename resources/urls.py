from django.urls import path

from .views.ResourceView import ResourceView

urlpatterns = [
    path(**{
        'route': '',
        'view': ResourceView.as_view({
            'get': 'list',
            'post': 'create',
        }),
        'name': 'resources_list',
    }),
    path(**{
        'route': '<int:pk>/',
        'view': ResourceView.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        'name': 'single_resource',
    }),
]
