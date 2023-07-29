import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from users.schema.TeacherType import TeacherType

from ..filtersets.CourseFilterSet import CourseFilterSet
from ..models.Course import Course
from .CategoryType import CategoryType
from .DiscountType import DiscountType


class CourseType(DjangoObjectType):
    teacher = graphene.Field(TeacherType)
    category = graphene.Field(CategoryType)
    discount = graphene.Field(DiscountType)
    body = graphene.String()
    progress = graphene.Float()
    learning_format = graphene.String()

    class Meta:
        model = Course
        interfaces = (relay.Node,)
        fields = (
            'id', 'teacher', 'title', 'price', 'count_lectures',
            'count_independents', 'count_listeners', 'duration',
            'category', 'preview', 'short_description', 'avg_rating',
            'created_at',
        )

    def resolve_teacher(self, info):
        return info.context.loaders.teacher_loader.load(self.teacher_id)

    def resolve_category(self, info):
        return info.context.loaders.category_loader.load(self.category_id)

    def resolve_body(self, info):
        return info.context.loaders.course_body_loader.load(self.id)

    def resolve_discount(self, info):
        return info.context.loaders.discount_loader.load(self.id)

    def resolve_learning_format(self, info):
        return self.get_learning_format_display()

    def resolve_preview(self, info):
        return info.context.build_absolute_uri(self.preview.url)

    @login_required
    def resolve_progress(self, info):
        return info.context.loaders.user_progress_loader.load(
            (self.id, info.context.user.id,)
        )


class CourseConnection(relay.Connection):
    class Meta:
        node = CourseType


class CourseQuery(graphene.ObjectType):
    course = relay.Node.Field(CourseType)
    all_courses = DjangoFilterConnectionField(CourseType,
                                              filterset_class=CourseFilterSet)
    latest_courses = relay.ConnectionField(CourseConnection)

    def resolve_all_courses(root, info, **kwargs):
        return Course.objects.filter(**{
            'is_published': True,
        })

    def resolve_latest_courses(root, info, **kwargs):
        return Course.objects.filter(**{
            'is_published': True,
        }).order_by('-created_at')
