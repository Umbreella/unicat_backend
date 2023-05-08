from django.urls import path, re_path

from .views.AnswerValueView import AnswerValueView
from .views.LessonCompleteView import LessonCompleteView
from .views.LessonTypeView import LessonTypeView
from .views.LessonView import LessonView
from .views.QuestionTypeView import QuestionTypeView
from .views.QuestionView import QuestionView
from .views.UserAnswerView import UserAnswerView
from .views.UserAttemptRefreshView import UserAttemptRefreshView
from .views.UserAttemptView import UserAttemptView

urlpatterns = [
    re_path(r'^(?P<lesson_id>[\w=]*)/attempt$', UserAttemptView.as_view(),
            name='user_attempt'),
    re_path(r'^(?P<lesson_id>[\w=]*)/attempt/refresh$',
            UserAttemptRefreshView.as_view(), name='user_attempt_refresh'),
    re_path(r'^(?P<lesson_id>[\w=]*)/complete$', LessonCompleteView.as_view(),
            name='lesson_complete'),
    re_path(r'^attempts/(?P<attempt_id>[\w=]*)/answer$',
            UserAnswerView.as_view(), name='user_answer'),
    path(**{
        'route': '',
        'view': LessonView.as_view({
            'get': 'list',
            'post': 'create',
        }),
        'name': 'lesson_list',
    }),
    path(**{
        'route': '<int:pk>/',
        'view': LessonView.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        'name': 'single_lesson',
    }),
    path(**{
        'route': 'types/',
        'view': LessonTypeView.as_view(),
        'name': 'lesson_types_list',
    }),
    path(**{
        'route': 'types/<int:pk>/',
        'view': LessonTypeView.as_view(),
        'name': 'single_lesson_type',
    }),
    path(**{
        'route': 'questions/',
        'view': QuestionView.as_view({
            'get': 'list',
            'post': 'create',
        }),
        'name': 'questions_list',
    }),
    path(**{
        'route': 'questions/<int:pk>/',
        'view': QuestionView.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        'name': 'single_question',
    }),
    path(**{
        'route': 'questions/types/',
        'view': QuestionTypeView.as_view(),
        'name': 'question_types_list',
    }),
    path(**{
        'route': 'questions/types/<int:pk>/',
        'view': QuestionTypeView.as_view(),
        'name': 'single_question_type',
    }),

    path(**{
        'route': 'questions/answers/',
        'view': AnswerValueView.as_view({
            'get': 'list',
            'post': 'create',
        }),
        'name': 'answers_list',
    }),
    path(**{
        'route': 'questions/answers/<int:pk>/',
        'view': AnswerValueView.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        'name': 'single_answer',
    }),
]
