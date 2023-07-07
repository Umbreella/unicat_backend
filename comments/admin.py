from django.contrib import admin

from .models.Comment import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('commented_type', 'commented_id', 'created_at', 'rating',)
    list_filter = ('commented_type', 'commented_id', 'created_at', 'rating',)
