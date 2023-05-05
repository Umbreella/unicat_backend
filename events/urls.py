from django.urls import path

from .views.EventView import EventView
from .views.NewView import NewView

urlpatterns = [
    path(**{
        'route': 'event/',
        'view': EventView.as_view({
            'get': 'list',
            'post': 'create',
        }),
        'name': 'event_list',
    }),
    path(**{
        'route': 'event/<int:pk>/',
        'view': EventView.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        'name': 'single_event',
    }),
    path(**{
        'route': 'news/',
        'view': NewView.as_view({
            'get': 'list',
            'post': 'create',
        }),
        'name': 'news_list',
    }),
    path(**{
        'route': 'news/<int:pk>/',
        'view': NewView.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        'name': 'single_new',
    }),
]
