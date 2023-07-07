import re

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .UserManager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(**{
        'max_length': 128,
        'unique': True,
        'help_text': 'User`s unique email address.',
    })
    password = models.CharField(**{
        'max_length': 128,
        'help_text': 'User password.',
    })
    first_name = models.CharField(**{
        'max_length': 128,
        'blank': True,
        'help_text': 'Username.',
    })
    last_name = models.CharField(**{
        'max_length': 128,
        'blank': True,
        'help_text': 'User`s last name.',
    })
    photo = models.ImageField(**{
        'upload_to': 'teachers/%Y/%m/%d/',
        'default': None,
        'null': True,
        'blank': True,
        'help_text': 'User Image.',
    })
    is_staff = models.BooleanField(**{
        'default': False,
        'help_text': 'Does the user have access to the administration panel.',
    })
    is_active = models.BooleanField(**{
        'default': False,
        'help_text': 'Is this account active.',
    })

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()

    objects = UserManager()

    def __str__(self):
        fullname = f'{self.first_name} {self.last_name}'

        if len(fullname) > 1:
            return fullname

        return self.email

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.strip()
        self.last_name = self.last_name.strip()
        self.email = self.email.strip()

        self.full_clean()

        current_password = self.password
        hashed_password_pattern = self.__get_hashed_pattern()

        if not re.fullmatch(hashed_password_pattern, current_password):
            self.set_password(current_password)

        super().save(*args, **kwargs)

    def __get_hashed_pattern(self):
        hash_algorithms = {
            'PBKDF2PasswordHasher': r'\w+[$]\d+[$]\w+[$].+',
            'MD5PasswordHasher': r'\w+[$]\w+[$].+',
        }

        password_hasher = settings.PASSWORD_HASHERS[0].split('.')[-1]
        current_hash = hash_algorithms.get(password_hasher)

        assert current_hash is not None, 'Not found password hasher'

        return current_hash
