import graphene

from courses.schema.CoursesType import CourseQuery
from users.schema.TeacherType import TeacherQuery


class GraphQLQuery(CourseQuery, TeacherQuery):
    pass


schema = graphene.Schema(query=GraphQLQuery)
