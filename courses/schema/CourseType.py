import graphene
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql.error import GraphQLError
from graphql_jwt.decorators import login_required

from ..filtersets.CourseFilterSet import CourseFilterSet
from ..models.Course import Course
from ..models.UserCourse import UserCourse
from .DiscountType import DiscountType


class CourseType(DjangoObjectType):
    learning_format = graphene.String()
    body = graphene.String()
    progress = graphene.Float()
    discount = graphene.Field(DiscountType)

    class Meta:
        model = Course
        interfaces = (relay.Node,)
        fields = ('id', 'teacher', 'title', 'price', 'count_lectures',
                  'count_independents', 'duration', 'category', 'preview',
                  'short_description', 'created_at', 'statistic',)

    # def resolve_teacher(root, info):
    #     key = root.teacher_id
    #     return info.context.loaders.teacher_by_course_loader.load(key)

    def resolve_learning_format(self, info):
        return self.get_learning_format_display()

    def resolve_preview(self, info):
        return info.context.build_absolute_uri(self.preview.url)

    def resolve_body(self, info):
        try:
            return self.course_body.body
        except ObjectDoesNotExist:
            return None

    def resolve_discount(self, info):
        return self.discounts.filter(**{
            'start_date__lte': timezone.now(),
            'end_date__gte': timezone.now(),
        }).first()

    @login_required
    def resolve_progress(self, info):
        try:
            user_course = UserCourse.objects.get(**{
                'course': self,
                'user': info.context.user,
            })
        except ObjectDoesNotExist:
            detail = 'You don`t have access on this course.'
            raise GraphQLError(detail)

        count_lessons = sum([
            self.count_lectures,
            self.count_independents,
        ])

        count_completed_lessons = sum([
            user_course.count_lectures_completed,
            user_course.count_independents_completed,
        ])

        progress = count_completed_lessons / count_lessons

        return round(progress * 100, 3)


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
