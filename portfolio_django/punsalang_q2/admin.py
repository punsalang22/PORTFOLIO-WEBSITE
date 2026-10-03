from django.contrib import admin
from .models import PersonalInformation, Project, TechStack

admin.site.register(PersonalInformation)


@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'tech_stack_names', 'link')
    filter_horizontal = ('tech_stack',)
