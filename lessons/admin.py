from django.contrib import admin
from django_summernote.admin import (SummernoteModelAdmin,
                                     SummernoteModelAdminMixin)

from .models.AnswerValue import AnswerValue
from .models.Lesson import Lesson
from .models.LessonBody import LessonBody
from .models.Question import Question
from .models.UserAnswer import UserAnswer
from .models.UserAttempt import UserAttempt
from .models.UserLesson import UserLesson


@admin.register(AnswerValue)
class AnswerValueAdmin(admin.ModelAdmin):
    list_display = ('question', 'value', 'is_true',)
    list_filter = ('question', 'is_true',)


class LessonBodyInline(SummernoteModelAdminMixin, admin.StackedInline):
    model = LessonBody
    summernote_fields = ('body',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'serial_number', 'parent', 'title',
                    'lesson_type', 'time_limit', 'count_questions',)
    list_filter = ('course', 'lesson_type',)
    inlines = (LessonBodyInline,)


@admin.register(LessonBody)
class LessonBodyAdmin(SummernoteModelAdmin):
    list_display = ('lesson',)
    summernote_fields = ('body',)


@admin.register(Question)
class QuestionAdmin(SummernoteModelAdmin):
    list_display = ('lesson', 'body', 'question_type',)
    summernote_fields = ('body',)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user_attempt', 'question', 'is_true',)


@admin.register(UserAttempt)
class UserAttemptAdmin(admin.ModelAdmin):
    list_display = ('user_lesson', 'time_start', 'time_end',
                    'count_true_answer',)


@admin.register(UserLesson)
class UserLessonAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'user',)
