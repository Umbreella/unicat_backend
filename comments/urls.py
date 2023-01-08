from django.urls import path

from .views.CommentCourseView import CommentCourseView
from .views.CommentEventView import CommentEventView
from .views.CommentNewsView import CommentNewsView

urlpatterns = [
    path('course', CommentCourseView.as_view(), name='comments-course'),
    path('news', CommentNewsView.as_view(), name='comments-news'),
    path('event', CommentEventView.as_view(), name='comments-event'),
]
