from django.urls import path

from .views.FeedbackView import FeedbackView

urlpatterns = [
    path(**{
        'route': '',
        'view': FeedbackView.as_view({
            'get': 'list',
            'post': 'create',
        }),
        'name': 'feedbacks_list',
    }),
    path(**{
        'route': '<int:pk>/',
        'view': FeedbackView.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
        }),
        'name': 'single_feedback',
    }),
]
