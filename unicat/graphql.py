import graphene
from django.conf import settings
from graphene_django.debug import DjangoDebug

from courses.schema.CategoryType import CategoryQuery
from courses.schema.CourseType import CourseQuery
from courses.schema.ShortLessonType import ShortLessonQuery
from events.schema.EventType import EventQuery
from events.schema.NewType import NewsQuery
from users.schema.TeacherType import TeacherQuery


class GraphQLQuery(CategoryQuery, CourseQuery, EventQuery, NewsQuery,
                   ShortLessonQuery, TeacherQuery):
    if settings.DEBUG:
        debug = graphene.Field(DjangoDebug, name='_debug')


schema = graphene.Schema(query=GraphQLQuery)
