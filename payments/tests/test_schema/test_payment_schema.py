from graphene import Context, NonNull, Schema, relay
from graphene.test import Client
from graphql_jwt.testcases import JSONWebTokenTestCase

from courses.models.Category import Category
from courses.models.Course import Course
from courses.models.LearningFormat import LearningFormat
from users.models import User
from users.models.Teacher import Teacher

from ...models.Payment import Payment
from ...schema.PaymentType import PaymentQuery, PaymentType


class PaymentTypeTestCase(JSONWebTokenTestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = PaymentType
        cls.model = Payment

        user = User.objects.create_user(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        teacher = Teacher.objects.create(**{
            'user': user,
            'description': 'q' * 50,
        })

        category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        first_course = Course.objects.create(**{
            'id': 1,
            'teacher': teacher,
            'title': 'q' * 50,
            'price': 50.0,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        second_course = Course.objects.create(**{
            'id': 2,
            'teacher': teacher,
            'title': 'q' * 50,
            'price': 50.0,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
        })

        Payment.objects.create(**{
            'id': 'q' * 27,
            'user': user,
            'course': first_course,
            'amount': 100.0,
            'is_success': True,
        })

        Payment.objects.create(**{
            'id': 'w' * 27,
            'user': user,
            'course': second_course,
            'amount': 100.0,
        })

        context = Context()
        context.user = user
        cls.context = context

    def setUp(self):
        schema = Schema(query=PaymentQuery)
        self.gql_client = Client(schema=schema)

    def test_Should_IncludeDefiniteDjangoModel(self):
        expected_model = self.model
        real_model = self.tested_class._meta.model

        self.assertEqual(expected_model, real_model)

    def test_Should_IncludeDefiniteInterfaces(self):
        expected_interfaces = [
            relay.Node,
        ]
        real_interfaces = list(self.tested_class._meta.interfaces)

        self.assertEqual(expected_interfaces, real_interfaces)

    def test_Should_IncludeAllFieldsFromModel(self):
        expected_fields = [
            'id', 'course', 'amount', 'created_at',
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'id': NonNull,
            'amount': NonNull,
            'created_at': NonNull,
        }
        real_fields = {
            key: value.type.__class__
            for key, value in self.tested_class._meta.fields.items()
        }

        all_fields_is_function = [
            callable(real_fields.pop(field)) for field in [
                'course',
            ]
        ]

        self.assertEqual(expected_fields, real_fields)
        self.assertTrue(all_fields_is_function)

    def test_When_SendQueryWithOutAuth_Should_ErrorHasNotPermission(self):
        response = self.client.execute(
            """
            query {
                myPayments {
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """,
        )

        expected_data = {
            'data': {
                'myPayments': None,
            },
            'errors': [
                {
                    'locations': [{'column': 17, 'line': 3, }, ],
                    'message': (
                        'You do not have permission to perform this action'
                    ),
                    'path': ['myPayments', ],
                },
            ],
        }
        real_data = response.formatted

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryForMyPayments_Should_ReturnDataWithOutErrors(self):
        response = self.gql_client.execute(
            """
            query {
                myPayments {
                    edges {
                        node {
                            id
                            course {
                                id
                            }
                        }
                    }
                }
            }
            """,
            context=self.context,
        )

        expected_data = {
            'data': {
                'myPayments': {
                    'edges': [
                        {
                            'node': {
                                'id': f'UGF5bWVudFR5cGU6c{"XFxc" * 8}XFx',
                                'course': {
                                    'id': 'Q291cnNlVHlwZTox',
                                },
                            },
                        },
                    ],
                },
            },
        }
        real_data = response

        self.assertEqual(expected_data, real_data)
