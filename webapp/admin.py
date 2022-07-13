from django.contrib import admin

# Register your models here.

from webapp.models import Issue, Status, Type


class IssuesAdmin(admin.ModelAdmin):
    list_display = ['summary', 'status']
    list_display_links = ['summary']
    list_filter = ['status', 'types']
    search_fields = ['summary']
    fields = ['summary', 'description', 'status', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Issue, IssuesAdmin)


class StatusesAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Status, StatusesAdmin)


class TypesAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Type, TypesAdmin)
