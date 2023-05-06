from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models.Category import Category
from .models.Course import Course
from .models.CourseBody import CourseBody
from .models.CourseStat import CourseStat
from .models.Discount import Discount
from .models.UserCourse import UserCourse


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'price', 'discount',
                    'learning_format', 'category',)
    list_filter = ('title', 'teacher', 'learning_format', 'category',)


@admin.register(CourseBody)
class CourseBodyAdmin(SummernoteModelAdmin):
    pass


@admin.register(CourseStat)
class CourseStatAdmin(admin.ModelAdmin):
    list_display = ('course', 'avg_rating', 'count_comments',
                    'count_five_rating', 'count_four_rating',
                    'count_three_rating', 'count_two_rating',
                    'count_one_rating',)
    list_filter = ('course', 'avg_rating', 'count_comments',
                   'count_five_rating', 'count_four_rating',
                   'count_three_rating', 'count_two_rating',
                   'count_one_rating',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass


@admin.register(UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'count_lectures_completed',
                    'count_independents_completed', 'last_view',)
