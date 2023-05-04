from django.urls import path

from .views.CommentView import CommentView
from .views.CreateCommentCourseView import CreateCommentCourseView
from .views.CreateCommentEventView import CreateCommentEventView
from .views.CreateCommentNewsView import CreateCommentNewsView

urlpatterns = [
    path('course/', CreateCommentCourseView.as_view(),
         name='create_comment_course'),
    path('event/', CreateCommentEventView.as_view(),
         name='create_comment_event'),
    path('news/', CreateCommentNewsView.as_view(),
         name='create_comment_news'),

    path(**{
        'route': '',
        'view': CommentView.as_view({
            'get': 'list',
        }),
        'name': 'comments',
    }),
    path(**{
        'route': '<int:pk>/',
        'view': CommentView.as_view({
            'get': 'retrieve',
            'delete': 'destroy',
        }),
        'name': 'single_comment',
    }),
]
