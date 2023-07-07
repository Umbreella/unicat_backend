from courses.loaders.CategoryLoader import CategoryLoader
from courses.loaders.CertificateTitleLoader import CertificateTitleLoader
from courses.loaders.CourseBodyLoader import CourseBodyLoader
from courses.loaders.DiscountLoader import DiscountLoader
from courses.loaders.UserProgressLoader import UserProgressLoader
from lessons.loaders.AnswerValueLoader import AnswerValueLoader
from lessons.loaders.PrivateChildrenLessonLoader import \
    PrivateChildrenLessonLoader
from lessons.loaders.PublicChildrenLessonLoader import \
    PublicChildrenLessonLoader
from lessons.loaders.UserLessonLoader import UserLessonLoader
from users.loaders.TeacherLoader import TeacherLoader
from users.loaders.UserLoader import UserLoader


class Loaders:
    def __init__(self):
        self.category_loader = CategoryLoader()
        self.course_body_loader = CourseBodyLoader()
        self.discount_loader = DiscountLoader()
        self.user_progress_loader = UserProgressLoader()
        self.user_loader = UserLoader()
        self.teacher_loader = TeacherLoader()
        self.certificate_loader = CertificateTitleLoader()
        self.public_children_loader = PublicChildrenLessonLoader()
        self.private_children_loader = PrivateChildrenLessonLoader()
        self.user_lesson_loader = UserLessonLoader()
        self.answer_value_loader = AnswerValueLoader()
