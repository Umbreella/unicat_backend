from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
# from django.contrib.auth.hashers import
from django.db import models

from .UserManager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)
    email = models.EmailField(max_length=128, unique=True)
    password = models.CharField(max_length=128)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()

    objects = UserManager()

    def __str__(self):
        if len(self.get_fullname()) > 1:
            return self.get_fullname()

        return self.get_email()

    def get_fullname(self):
        return f'{self.first_name} {self.last_name}'

    def get_email(self):
        return self.email
