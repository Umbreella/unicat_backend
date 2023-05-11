from django.contrib import admin

from .models.Resource import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    pass
