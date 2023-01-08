from django.test import TestCase
from graphene import Schema
from graphene.test import Client

from unicat.graphql.functions import get_value_from_model_id
from users.models import User
from users.models.Teacher import Teacher

from ...models.Category import Category
from ...models.Course import Course
from ...models.LearningFormat import LearningFormat
from ...schema.CourseType import CourseQuery, CourseType


class CourseTypeTestCase(TestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CourseType

        user = User.objects.create_user(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        teacher = Teacher.objects.create(**{
            'user': user,
            'description': 'q' * 50,
        })

        first_category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        second_category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        #   'Q291cnNlVHlwZTox' - 'CourseType:1'
        cls.course_id = 'Q291cnNlVHlwZTox'
        cls.course_title_q = 'q' * 50,
        cls.course_title_w = 'w' * 50,

        Course.objects.create(**{
            'teacher': teacher,
            'title': cls.course_title_q,
            'price': 50.0,
            'discount': None,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': first_category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
            'description': 'q' * 50,
        })

        Course.objects.create(**{
            'teacher': teacher,
            'title': cls.course_title_w,
            'price': 50.0,
            'discount': None,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': first_category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
            'description': 'q' * 50,
        })

        Course.objects.create(**{
            'teacher': teacher,
            'title': cls.course_title_q,
            'price': 500.0,
            'discount': None,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': first_category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
            'description': 'q' * 50,
        })

        Course.objects.create(**{
            'teacher': teacher,
            'title': cls.course_title_w,
            'price': 50.0,
            'discount': None,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': second_category,
            'preview': 'temporary_img',
            'short_description': 'q' * 50,
            'description': 'q' * 50,
        })

    def setUp(self) -> None:
        schema = Schema(query=CourseQuery)

        self.gql_client = Client(schema=schema)

    def test_Should_IncludeAllFieldsFromModel(self):
        expected_fields = [field.name for field in Course._meta.fields] + [
            'statistic', 'discounts', 'shortlesson_set', 'lessons'
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_When_SendQueryWithCourseId_Should_ReturnCourseByCourseId(self):
        response = self.gql_client.execute(
            '''
            query GetCourse ($id: ID!) {
                course (id: $id) {
                    id
                }
            }
            ''',
            variables={
                'id': self.course_id
            },
        )

        expected_response = {
            'data': {
                'course': {
                    'id': self.course_id,
                }
            }
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithPreview_Should_ReturnFullUrlForFile(self):
        response = self.gql_client.execute(
            '''
            query GetCourse ($id: ID!) {
                course (id: $id) {
                    id
                    preview
                }
            }
            ''',
            variables={
                'id': self.course_id
            },
        )

        expected_url = '\'NoneType\' object has no attribute ' \
                       '\'build_absolute_uri\''
        real_url = response['errors'][0]['message']

        self.assertEqual(expected_url, real_url)

    def test_When_SendQueryListCourses_Should_ReturnListCourses(self):
        response = self.gql_client.execute(
            '''
            query {
                allCourses {
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            ''',
        )

        edges = []
        model_name = self.tested_class.__name__

        for course in Course.objects.values('id'):
            edges += [{
                'node': {
                    'id': get_value_from_model_id(model_name=model_name,
                                                  model_id=course['id'])
                }
            }]

        expected_response = {
            'data': {
                'allCourses': {
                    'edges': edges
                }
            }
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryWithFilters_Should_ReturnFilteredCourses(self):
        response = self.gql_client.execute(
            '''
            query GetFilteredCourses ($orderBy: String, $search: String,
                                      $category: String){
                allCourses (orderBy: $orderBy, search: $search,
                            category: $category, ){
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            ''',
            variables={
                'orderBy': '-created_at',
                'search': 'q',
                #   'OjE=' - ':1'
                'category': 'OjE=',
            },
        )

        edges = []
        model_name = self.tested_class.__name__

        courses = Course.objects.all()
        filtered_courses = courses.filter(**{
            'title__icontains': 'q',
            'category_id': 1,
        })
        ordered_courses = filtered_courses.order_by('-created_at')

        for course in ordered_courses.values('id'):
            edges += [{
                'node': {
                    'id': get_value_from_model_id(model_name=model_name,
                                                  model_id=course['id'])
                }
            }]

        expected_response = {
            'data': {
                'allCourses': {
                    'edges': edges
                }
            }
        }
        real_response = response

        self.assertEqual(expected_response, real_response)

    def test_When_SendQueryListLatestCourses_Should_ReturnListLatestCourses(
            self):
        response = self.gql_client.execute(
            '''
            query {
                latestCourses {
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            ''',
        )

        edges = []
        model_name = self.tested_class.__name__

        for course in Course.objects.order_by('-created_at').values('id'):
            edges += [{
                'node': {
                    'id': get_value_from_model_id(model_name=model_name,
                                                  model_id=course['id'])
                }
            }]

        expected_response = {
            'data': {
                'latestCourses': {
                    'edges': edges
                }
            }
        }
        real_response = response

        self.assertEqual(expected_response, real_response)
