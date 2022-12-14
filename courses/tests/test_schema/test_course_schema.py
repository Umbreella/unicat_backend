import json
import tempfile

from django.conf import settings
from graphene_django.utils import GraphQLTestCase

from users.models import User
from users.models.Teacher import Teacher

from ...models.Category import Category
from ...models.Course import Course
from ...models.LearningFormat import LearningFormat


class CourseTypeTestCase(GraphQLTestCase):
    databases = {'master'}

    @classmethod
    def setUpTestData(cls):
        temporary_img = tempfile.NamedTemporaryFile(suffix=".jpg").name

        user = User.objects.create_user(**{
            'email': 'q' * 50 + '@q.qq',
            'password': 'q' * 50,
        })

        teacher = Teacher.objects.create(**{
            'user': user,
            'photo': temporary_img,
            'description': 'q' * 50,
        })

        category = Category.objects.create(**{
            'title': 'q' * 50,
        })

        Course.objects.create(**{
            'teacher': teacher,
            'title': 'q' * 50,
            'price': 50.0,
            'discount': None,
            'count_lectures': 50,
            'count_independents': 50,
            'duration': 50,
            'learning_format': LearningFormat.REMOTE,
            'category': category,
            'preview': temporary_img,
            'short_description': 'q' * 50,
            'description': 'q' * 50,
        })

        cls.course_id = 'Q291cnNlVHlwZTox'

    def test_When_SendQueryWithAllFields_Should_ReturnAllFields(self):
        response = self.query(
            '''
            query {
                course (id: "''' + self.course_id + '''" ) {
                    id
                    title
                    price
                    discount
                    countLectures
                    countIndependents
                    duration
                    learningFormat
                    preview
                    shortDescription
                    description
                    category {
                        id
                    }
                    teacher {
                        id
                    }
                }
            }
            ''',
        )

        self.assertResponseNoErrors(response)

    def test_When_SendQueryWithPreview_Should_ReturnFullUrlForFile(self):
        response = self.query(
            '''
            query {
                course (id: "''' + self.course_id + '''" ) {
                    preview
                }
            }
            ''',
        )

        content = json.loads(response.content)

        expected_url = 'http://testserver' + settings.MEDIA_URL
        real_url = content['data']['course']['preview']

        self.assertIn(expected_url, real_url)

    def test_When_SendQueryListWithAllFields_Should_ReturnAllFields(self):
        response = self.query(
            '''
            query {
                allCourses {
                    edges {
                        node {
                            id
                            title
                            price
                            discount
                            countLectures
                            countIndependents
                            duration
                            learningFormat
                            preview
                            shortDescription
                            description
                            category {
                                id
                            }
                            teacher {
                                id
                            }
                        }
                    }
                }
            }
            ''',
        )

        content = json.loads(response.content)

        expected_count_course = len(Course.objects.all())
        real_count_course = len(content['data']['allCourses']['edges'])

        self.assertResponseNoErrors(response)
        self.assertEqual(expected_count_course, real_count_course)
