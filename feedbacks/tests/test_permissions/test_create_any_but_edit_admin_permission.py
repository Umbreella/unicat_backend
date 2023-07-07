from django.test import TestCase

from unicat.permissions.DjModelPermForDRF import DjModelPermForDRF
from users.models import User

from ...models.Feedback import Feedback
from ...permissions.CreateAnyButEditAdminPermission import \
    CreateAnyButEditAdminPermission


class CreateAnyButEditAdminPermissionTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CreateAnyButEditAdminPermission

        cls.user = User.objects.create_user(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
            'is_active': True,
            'is_staff': True,
        })

        Feedback.objects.create(**{
            'id': 1,
            'name': 'q' * 50,
            'email': 'q' * 50 + '@q.qq',
            'body': 'q' * 50,
        })

        cls.methods = {
            'GET': 'view_feedback',
            'PUT': 'change_feedback',
            'DELETE': 'delete_feedback',
        }

        cls.view = type('view', (object,), {
            'get_queryset': lambda: Feedback.objects.filter(id=1),
        })

    def setUp(self):
        self.request = type('request', (object,), {
            'method': 'POST',
            'user': self.user,
        })

    def test_Should_InheritCertainClasses(self):
        expected_classes = (
            DjModelPermForDRF,
        )
        real_classes = self.tested_class.__bases__

        self.assertEqual(expected_classes, real_classes)

    def test_Should_OverrideSuperMethodHasPermission(self):
        expected_method = DjModelPermForDRF.has_permission
        real_method = self.tested_class.has_permission

        self.assertNotEqual(expected_method, real_method)

    def test_When_UserHasNotPermissions_Should_ReturnSuperMethodData(self):
        request = self.request

        permission_class = self.tested_class()

        expected_data = {
            'GET': False,
            'PUT': False,
            'DELETE': False,
        }

        real_data = {}
        for key in self.methods.keys():
            request.method = key

            real_data.update({
                key: permission_class.has_permission(request, self.view)
            })

        self.assertEqual(expected_data, real_data)

    def test_When_GetMethodAndAnonymousUser_Should_ReturnFalse(self):
        request = self.request
        request.method = 'GET'
        request.user = None

        permission_class = self.tested_class()

        expected_data = False
        real_data = permission_class.has_permission(request, self.view)

        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodAndAnonymousUser_Should_ReturnTrue(self):
        request = self.request
        request.user = None

        permission_class = self.tested_class()

        expected_data = True
        real_data = permission_class.has_permission(request, self.view)

        self.assertEqual(expected_data, real_data)
