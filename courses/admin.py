from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models.Category import Category
from .models.Course import Course


@admin.register(Course)
class CourseAdmin(SummernoteModelAdmin):
    summernote_fields = ('description', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
