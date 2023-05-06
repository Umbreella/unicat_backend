from django.contrib import admin

from .models.Feedback import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    pass
