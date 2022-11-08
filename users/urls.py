from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView

from .views.ChangeDataUserView import ChangeDataUserView
from .views.LoginUserView import LoginUserView
from .views.RegistrationUserView import RegistrationUserView

urlpatterns = [
    path('signin', LoginUserView.as_view(), name='signin'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/destroy', TokenBlacklistView.as_view(), name='token_destroy'),
    path('signup', RegistrationUserView.as_view(), name='signup'),
    path('change', ChangeDataUserView.as_view(), name='change'),
]
