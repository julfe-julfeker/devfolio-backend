from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_featured", "completed_date")
    search_fields = ("title", "summary")
    list_filter = ("category", "is_featured")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tech_stack",)