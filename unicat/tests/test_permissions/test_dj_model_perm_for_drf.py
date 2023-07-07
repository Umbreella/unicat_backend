from unittest import TestCase

from rest_framework.permissions import DjangoModelPermissions

from ...permissions.DjModelPermForDRF import DjModelPermForDRF


class DjModelPermForDRFTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tested_class = DjModelPermForDRF

    def test_Should_InheritDefiniteSuper(self):
        expected_bases = (
            DjangoModelPermissions,
        )
        real_bases = self.tested_class.__bases__

        self.assertEqual(expected_bases, real_bases)

    def test_Should_OverrideSuperAttr(self):
        expected_bases = DjangoModelPermissions.perms_map
        real_bases = self.tested_class.perms_map

        self.assertNotEqual(expected_bases, real_bases)

    def test_Should_DontOverrideSuperMethods(self):
        expected_methods = [
            DjangoModelPermissions.get_required_permissions,
            DjangoModelPermissions.has_permission,
        ]
        real_methods = [
            self.tested_class.get_required_permissions,
            self.tested_class.has_permission,
        ]

        self.assertEqual(expected_methods, real_methods)
