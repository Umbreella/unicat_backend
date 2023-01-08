from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models.Event import Event
from .models.New import New


@admin.register(Event)
class EventAdmin(SummernoteModelAdmin):
    summernote_fields = ('description', )


@admin.register(New)
class NewsAdmin(SummernoteModelAdmin):
    summernote_fields = ('description', )
    list_display = ('title', 'author', 'created_at')
    list_filter = ('author', 'created_at')
