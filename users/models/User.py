import re

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .UserManager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)
    photo = models.ImageField(upload_to='teachers/%Y/%m/%d/', default=None,
                              null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()

    objects = UserManager()

    def __str__(self):
        if len(self.get_fullname()) > 1:
            return self.get_fullname()

        return self.email

    def get_fullname(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        self.full_clean()

        current_password = self.password
        hashed_password_pattern = self.__get_hashed_pattern()

        if not re.fullmatch(hashed_password_pattern, current_password):
            self.set_password(current_password)

        self.first_name = str(self.first_name).strip()
        self.last_name = str(self.last_name).strip()
        self.email = str(self.email).strip()

        super().save(*args, **kwargs)

    def __get_hashed_pattern(self):
        current_hash_algorithm = settings.PASSWORD_HASHERS[0]

        if 'PBKDF2PasswordHasher' in current_hash_algorithm:
            return r'\w+[$]\d+[$]\w+[$].+'

        if 'MD5PasswordHasher' in current_hash_algorithm:
            return r'\w+[$]\w+[$].+'
