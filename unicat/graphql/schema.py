import graphene

from comments.schema.CommentType import CommentQuery
from courses.schema.CategoryType import CategoryQuery
from courses.schema.CourseStatType import CourseStatQuery
from courses.schema.CourseType import CourseQuery
from courses.schema.UserCertificateType import UserCertificateQuery
from courses.schema.UserCourseType import UserCourseQuery
from events.schema.EventType import EventQuery
from events.schema.NewType import NewsQuery
from lessons.schema.LessonType import LessonQuery
from lessons.schema.PrivateParentLessonType import PrivateParentLessonQuery
from lessons.schema.PublicParentLessonType import PublicParentLessonQuery
from lessons.schema.QuestionType import QuestionQuery
from lessons.schema.UserAttemptType import UserAttemptQuery
from lessons.schema.UserLessonType import UserLessonQuery
from payments.schema.PaymentType import PaymentQuery
from users.schema.TeacherType import TeacherQuery


class GraphQLQuery(CategoryQuery, CourseQuery, CourseStatQuery,
                   PrivateParentLessonQuery, PublicParentLessonQuery,
                   LessonQuery, UserAttemptQuery, QuestionQuery,
                   UserCourseQuery, UserCertificateQuery, UserLessonQuery,
                   CommentQuery, EventQuery, NewsQuery, TeacherQuery,
                   PaymentQuery):
    pass


schema = graphene.Schema(query=GraphQLQuery)
