from django.contrib import admin
from .models import Profile, Skill, Experience, Education

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "headline", "email", "is_available_for_hire")
    search_fields = ("full_name", "headline", "email")

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "proficiency", "is_featured")
    search_fields = ("name",)
    list_filter = ("category", "is_featured")

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("company", "role", "start_date", "is_current")
    search_fields = ("company", "role")
    list_filter = ("employment_type", "is_current")

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("institution", "degree", "start_year", "end_year")
    search_fields = ("institution", "degree")