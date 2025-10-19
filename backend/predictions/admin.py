from django.contrib import admin
from .models import PredictionSession, ModelPrediction, PredictionResult, ComparativeAnalysis


@admin.register(PredictionSession)
class PredictionSessionAdmin(admin.ModelAdmin):
    list_display = [
        'session_id', 'user', 'domain', 'input_type', 'status', 
        'confidence_score', 'created_at', 'completed_at'
    ]
    list_filter = ['status', 'domain', 'input_type', 'created_at']
    search_fields = ['session_id', 'user__username', 'domain', 'input_type']
    readonly_fields = ['session_id', 'created_at', 'updated_at', 'completed_at']
    fieldsets = (
        ('Session Information', {
            'fields': ('session_id', 'user', 'domain', 'input_type', 'status')
        }),
        ('Input Data', {
            'fields': ('input_file_path', 'input_metadata')
        }),
        ('Results', {
            'fields': ('aggregated_result', 'confidence_score')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ModelPrediction)
class ModelPredictionAdmin(admin.ModelAdmin):
    list_display = [
        'session', 'model', 'status', 'confidence_score', 
        'processing_time', 'created_at', 'completed_at'
    ]
    list_filter = ['status', 'model__domain', 'model__framework', 'created_at']
    search_fields = ['session__session_id', 'model__name', 'error_message']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    fieldsets = (
        ('Prediction Information', {
            'fields': ('session', 'model', 'status')
        }),
        ('Results', {
            'fields': ('prediction_result', 'confidence_score', 'processing_time')
        }),
        ('Error Information', {
            'fields': ('error_message', 'error_details'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PredictionResult)
class PredictionResultAdmin(admin.ModelAdmin):
    list_display = [
        'prediction', 'predicted_class', 'uncertainty_score', 
        'model_version', 'created_at'
    ]
    list_filter = ['model_version', 'created_at']
    search_fields = ['prediction__model__name', 'predicted_class']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Result Information', {
            'fields': ('prediction', 'predicted_class', 'class_probabilities')
        }),
        ('Raw Data', {
            'fields': ('raw_output', 'attention_weights'),
            'classes': ('collapse',)
        }),
        ('Metrics', {
            'fields': ('uncertainty_score', 'model_version', 'preprocessing_applied')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ComparativeAnalysis)
class ComparativeAnalysisAdmin(admin.ModelAdmin):
    list_display = [
        'session', 'consensus_score', 'created_at'
    ]
    list_filter = ['created_at']
    search_fields = ['session__session_id']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Analysis Results', {
            'fields': ('session', 'majority_vote', 'weighted_average', 'consensus_score')
        }),
        ('Detailed Analysis', {
            'fields': ('agreement_matrix', 'disagreement_analysis', 'confidence_intervals', 'statistical_significance'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
