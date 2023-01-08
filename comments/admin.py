from django.contrib import admin

from .models.Comment import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('commented_type', 'commented_id', 'created_at',
                    'count_like', 'rating')
    list_filter = ('commented_type', 'commented_id', 'created_at',
                   'count_like', 'rating')

    def delete_queryset(self, request, queryset):
        for item in queryset:
            item.delete()

        # lookup = {
        #     'commented_type': CommentedType.COURSE.value
        # }
        #
        # course_queryset = queryset.filter(**lookup)
        #
        # if course_queryset.exists():
        #     for item in course_queryset:
        #         item.delete()
        #
        # queryset.delete()
