from django.contrib import admin

from .models import User
from .models.Teacher import Teacher


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass
