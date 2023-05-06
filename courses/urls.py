from django.urls import path, re_path

from .views.CategoryView import CategoryView
from .views.CourseView import CourseView
from .views.DiscountView import DiscountView
from .views.LearningFormatView import LearningFormatView
from .views.UserCertificateView import UserCertificateView

urlpatterns = [
    path(**{
        'route': 'category/',
        'view': CategoryView.as_view({
            'get': 'list',
            'post': 'create',
        }),
        'name': 'category_list',
    }),
    path(**{
        'route': 'category/<int:pk>/',
        'view': CategoryView.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        'name': 'single_category',
    }),
    path(**{
        'route': '',
        'view': CourseView.as_view({
            'get': 'list',
            'post': 'create',
        }),
        'name': 'course_list',
    }),
    path(**{
        'route': '<int:pk>/',
        'view': CourseView.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        'name': 'single_course',
    }),
    path(**{
        'route': 'discounts/',
        'view': DiscountView.as_view({
            'get': 'list',
            'post': 'create',
        }),
        'name': 'discount_list',
    }),
    path(**{
        'route': 'discounts/<int:pk>/',
        'view': DiscountView.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        'name': 'single_discount',
    }),
    path(**{
        'route': 'formats/',
        'view': LearningFormatView.as_view(),
        'name': 'learning_formats_list',
    }),
    path(**{
        'route': 'formats/<int:pk>/',
        'view': LearningFormatView.as_view(),
        'name': 'single_learning_formats',
    }),

    re_path(r'^(?P<course_id>[\w=]*)/certificate$',
            UserCertificateView.as_view(), name='user_certificate'),
]
