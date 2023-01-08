import graphene
from django.core.cache import cache
from graphene import relay
from graphene.types import generic
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.utils import base64

from ..filtersets.CourseFilterSet import CourseFilterSet
from ..models.Course import Course
from ..models.CourseStat import CourseStat
from ..models.ShortLesson import ShortLesson


class CourseStatType(DjangoObjectType):
    class Meta:
        model = CourseStat
        interfaces = (relay.Node,)
        fields = '__all__'


class CourseType(DjangoObjectType):
    lessons = generic.GenericScalar()
    # teacher = graphene.List(TeacherType)

    class Meta:
        model = Course
        interfaces = (relay.Node,)
        fields = '__all__'

    # def resolve_teacher(root, info):
    #     key = root.teacher_id
    #     return info.context.loaders.teacher_by_course_loader.load(key)

    def resolve_preview(self, info):
        return info.context.build_absolute_uri(self.preview.url)

    def resolve_lessons(self, info):
        cache_key = f'course_{self.id}_lessons_all'
        cached_value = cache.get(cache_key, None)

        if cached_value:
            return cached_value

        query = 'WITH RECURSIVE cte AS (' \
                '   SELECT startTable.id, startTable.serial_number, ' \
                '       startTable.title, startTable.parent_lesson_id ' \
                '   FROM public.courses_shortlesson AS startTable' \
                f'	WHERE startTable.course_id = {self.id}' \
                '	' \
                '   UNION ' \
                '   ' \
                '   SELECT mainTable.id, mainTable.serial_number, ' \
                '       mainTable.title, mainTable.parent_lesson_id ' \
                '   	FROM public.courses_shortlesson AS mainTable' \
                '		JOIN cte ' \
                '		    ON mainTable.parent_lesson_id = cte.id' \
                ')' \
                'SELECT * ' \
                'FROM cte ' \
                'ORDER BY parent_lesson_id NULLS FIRST, serial_number'

        result_query = ShortLesson.objects.raw(query)
        data = list(map(lambda item: dict(item), result_query))

        data_tree = CourseType.create_tree(data)
        cache.set(cache_key, data_tree)

        return data_tree

    @staticmethod
    def create_tree(data_list, parent_id=None):
        filtered_data = filter(
            lambda item: item.get('parent_lesson_id', None) == parent_id,
            data_list)
        filtered_list = list(filtered_data)

        for item in filtered_list:
            item['childs'] = CourseType.create_tree(data_list, item['id'])
            item.update({
                'id': base64(f'ShortLessonType:{item["id"]}'),
            })
            del item['parent_lesson_id']

        return filtered_list


class CourseConnection(relay.Connection):
    class Meta:
        node = CourseType


class CourseQuery(graphene.ObjectType):
    course = relay.Node.Field(CourseType)
    all_courses = DjangoFilterConnectionField(CourseType,
                                              filterset_class=CourseFilterSet)
    latest_courses = relay.ConnectionField(CourseConnection)

    def resolve_latest_courses(root, info, **kwargs):
        return Course.objects.order_by('-created_at')
