from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views.ConfirmEmailView import ConfirmEmailView
from .views.ConfirmNewEmailView import ConfirmNewEmailView
from .views.GroupView import GroupView
from .views.LoginUserView import LoginUserView
from .views.LogoutUserView import LogoutUserView
from .views.PermissionView import PermissionView
from .views.ProfileView import ProfileView
from .views.RegistrationUserView import RegistrationUserView
from .views.ResetPasswordView import ResetPasswordView
from .views.TeacherView import TeacherView
from .views.UpdatePasswordView import UpdatePasswordView
from .views.UserView import UserView

urlpatterns = [
    path('signin', LoginUserView.as_view(), name='signin'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/destroy', LogoutUserView.as_view(), name='token_destroy'),
    path('signup', RegistrationUserView.as_view(), name='signup'),
    path('password/reset/', ResetPasswordView.as_view(),
         name='password_reset'),
    path('password/update/', UpdatePasswordView.as_view(),
         name='password_update'),
    path('profile/', ProfileView.as_view(), name='my_profile'),
    path('email/confirm/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('email/update/', ConfirmNewEmailView.as_view(), name='update_email'),

    path(**{
        'route': '',
        'view': UserView.as_view({
            'get': 'list',
            'post': 'create',
        }),
        'name': 'user_list',
    }),
    path(**{
        'route': '<int:pk>/',
        'view': UserView.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        'name': 'single_user',
    }),
    path(**{
        'route': 'teachers/',
        'view': TeacherView.as_view({
            'get': 'list',
            'post': 'create',
        }),
        'name': 'teacher_list',
    }),
    path(**{
        'route': 'teachers/<int:pk>/',
        'view': TeacherView.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        'name': 'single_teacher',
    }),
    path(**{
        'route': 'groups/',
        'view': GroupView.as_view({
            'get': 'list',
            'post': 'create',
        }),
        'name': 'groups_list',
    }),
    path(**{
        'route': 'groups/<int:pk>/',
        'view': GroupView.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        'name': 'single_group',
    }),
    path(**{
        'route': 'permissions/',
        'view': PermissionView.as_view({
            'get': 'list',
        }),
        'name': 'permissions_list',
    }),
    path(**{
        'route': 'permissions/<int:pk>/',
        'view': PermissionView.as_view({
            'get': 'retrieve',
        }),
        'name': 'single_permission',
    }),
]
