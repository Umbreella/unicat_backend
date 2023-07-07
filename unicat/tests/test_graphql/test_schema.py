from unittest import TestCase

import graphene

from ...graphql import schema


class SchemaTestCase(TestCase):
    def test_Should_IncludeVariableSchema(self):
        expected_class = graphene.Schema
        real_schema = schema.schema.__class__

        self.assertEqual(expected_class, real_schema)
