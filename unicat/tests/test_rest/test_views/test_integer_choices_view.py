from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.test import APITestCase

from users.models import User

from ....rest.serializers.IntegerChoicesSerializer import \
    IntegerChoicesSerializer
from ....rest.views.IntegerChoicesView import IntegerChoiceView


class ResourceViewTestCase(APITestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = IntegerChoiceView
        cls.serializer = IntegerChoicesSerializer

        cls.user = User.objects.create_superuser(**{
            'id': 1,
            'email': 'test@email.com',
            'password': 'password',
        })

        client = cls.client_class()
        client.force_authenticate(user=cls.user)
        cls.logged_client = client

    def test_Should_InheritModelViewSet(self):
        expected_super_classes = (
            RetrieveAPIView,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_PermissionClassesIsAdminUser(self):
        expected_permission_classes = (
            IsAdminUser,
        )
        real_permission_classes = self.tested_class.permission_classes

        self.assertEqual(expected_permission_classes, real_permission_classes)

    def test_Should_SerializerClassIsResourceSerializer(self):
        expected_serializer = self.serializer
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)
