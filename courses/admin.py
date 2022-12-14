from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ImportExportModelAdmin

from .models.Category import Category
from .models.Course import Course
from .models.Discount import Discount
from .models.ShortLesson import ShortLesson


@admin.register(Course)
class CourseAdmin(SummernoteModelAdmin):
    summernote_fields = ('description', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass


@admin.register(ShortLesson)
class ShortLessonAdmin(ImportExportModelAdmin):
    pass
