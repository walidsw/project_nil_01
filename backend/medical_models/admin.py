from django.contrib import admin
from .models import MedicalDomain, InputType, ResearchPaper, MedicalModel, ModelCategory


@admin.register(MedicalDomain)
class MedicalDomainAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']


@admin.register(InputType)
class InputTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'file_extension', 'is_image', 'is_structured']
    search_fields = ['name', 'description']
    list_filter = ['is_image', 'is_structured']


@admin.register(ResearchPaper)
class ResearchPaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'authors', 'journal', 'year', 'doi']
    search_fields = ['title', 'authors', 'journal', 'doi', 'arxiv_id']
    list_filter = ['year', 'journal']
    ordering = ['-year', 'title']


@admin.register(MedicalModel)
class MedicalModelAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'domain', 'input_type', 'accuracy', 'status', 
        'version', 'framework', 'created_at'
    ]
    list_filter = [
        'domain', 'input_type', 'status', 'framework', 'created_at'
    ]
    search_fields = ['name', 'description', 'domain__name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'domain', 'input_type', 'research_paper')
        }),
        ('Performance Metrics', {
            'fields': ('accuracy', 'precision', 'recall', 'f1_score')
        }),
        ('Model Configuration', {
            'fields': ('model_file_path', 'preprocessing_config', 'output_classes', 'framework')
        }),
        ('Status & Version', {
            'fields': ('status', 'version', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ModelCategory)
class ModelCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'domain', 'description']
    list_filter = ['domain']
    search_fields = ['name', 'description', 'domain__name']
    filter_horizontal = ['models']
