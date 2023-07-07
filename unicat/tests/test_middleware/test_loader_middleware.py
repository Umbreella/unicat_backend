from unittest import TestCase

from ...graphql.loaders import Loaders
from ...middleware.LoaderMiddleware import LoaderMiddleware


class LoaderMiddlewareTestCase(TestCase):
    def setUp(self) -> None:
        def next(root, info, **kwargs):
            return info.context

        self.next = next
        self.info = type('info', (object,), {
            'context': type('context', (object,), {}),
        })

    def test_Should_IncludeMethodResolve(self):
        expected_value = True
        real_value = hasattr(LoaderMiddleware, 'resolve')

        self.assertEqual(expected_value, real_value)

    def test_When_UseResolver_Should_AddLoadersContext(self):
        context = LoaderMiddleware().resolve(self.next, None, self.info)

        expected_context = True
        real_context = hasattr(context, 'loaders')

        expected_class = Loaders
        real_class = context.loaders.__class__

        self.assertEqual(expected_context, real_context)
        self.assertEqual(expected_class, real_class)

    def test_When_InfoHasContext_Should_DontChangeLoaders(self):
        resolver = LoaderMiddleware().resolve

        expected_loaders = resolver(self.next, None, self.info).loaders
        real_loaders = resolver(self.next, None, self.info).loaders

        self.assertEqual(expected_loaders, real_loaders)
