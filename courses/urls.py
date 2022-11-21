from django.urls import path

from .views.CoursesView import CourseView

urlpatterns = [
    path('', CourseView.as_view({'get': 'list'}), name='all_courses'),
    path('<int:pk>', CourseView.as_view({'get': 'retrieve'}),
         name='all_courses'),
]
