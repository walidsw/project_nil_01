from rest_framework import serializers
from django.core.files.uploadedfile import UploadedFile
from .models import PredictionSession, ModelPrediction, PredictionResult, ComparativeAnalysis
from medical_models.serializers import MedicalModelListSerializer


class PredictionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionResult
        fields = [
            'id', 'raw_output', 'predicted_class', 'class_probabilities',
            'uncertainty_score', 'attention_weights', 'model_version',
            'preprocessing_applied', 'created_at'
        ]
        read_only_fields = ['created_at']


class ModelPredictionSerializer(serializers.ModelSerializer):
    model = MedicalModelListSerializer(read_only=True)
    detailed_result = PredictionResultSerializer(read_only=True)
    
    class Meta:
        model = ModelPrediction
        fields = [
            'id', 'model', 'status', 'prediction_result', 'confidence_score',
            'processing_time', 'error_message', 'error_details', 'created_at',
            'updated_at', 'completed_at', 'detailed_result'
        ]
        read_only_fields = ['created_at', 'updated_at', 'completed_at']


class ComparativeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComparativeAnalysis
        fields = [
            'id', 'majority_vote', 'weighted_average', 'consensus_score',
            'agreement_matrix', 'disagreement_analysis', 'confidence_intervals',
            'statistical_significance', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class PredictionSessionSerializer(serializers.ModelSerializer):
    predictions = ModelPredictionSerializer(many=True, read_only=True)
    comparative_analysis = ComparativeAnalysisSerializer(read_only=True)
    
    class Meta:
        model = PredictionSession
        fields = [
            'id', 'session_id', 'domain', 'input_type', 'status',
            'input_metadata', 'aggregated_result', 'confidence_score',
            'created_at', 'updated_at', 'completed_at', 'predictions',
            'comparative_analysis'
        ]
        read_only_fields = ['session_id', 'created_at', 'updated_at', 'completed_at']


class PredictionSessionListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    prediction_count = serializers.SerializerMethodField()
    completed_count = serializers.SerializerMethodField()
    
    class Meta:
        model = PredictionSession
        fields = [
            'id', 'session_id', 'domain', 'input_type', 'status',
            'confidence_score', 'created_at', 'completed_at',
            'prediction_count', 'completed_count'
        ]
    
    def get_prediction_count(self, obj):
        return obj.predictions.count()
    
    def get_completed_count(self, obj):
        return obj.predictions.filter(status='completed').count()


class PredictionRequestSerializer(serializers.Serializer):
    """Serializer for prediction requests"""
    domain = serializers.CharField(max_length=100)
    input_type = serializers.CharField(max_length=50)
    category_id = serializers.IntegerField(required=False)
    
    def validate_domain(self, value):
        from medical_models.models import MedicalDomain
        if not MedicalDomain.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Invalid domain")
        return value
    
    def validate_input_type(self, value):
        from medical_models.models import InputType
        if not InputType.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Invalid input type")
        return value


class FileUploadSerializer(serializers.Serializer):
    """Serializer for file uploads"""
    file = serializers.FileField()
    domain = serializers.CharField(max_length=100)
    input_type = serializers.CharField(max_length=50)
    metadata = serializers.JSONField(required=False, default=dict)
    
    def validate_file(self, value):
        # Check file size (50MB limit)
        if value.size > 50 * 1024 * 1024:
            raise serializers.ValidationError("File size cannot exceed 50MB")
        
        # Check file extension
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.nii', '.nii.gz', '.csv', '.json']
        file_extension = '.' + value.name.split('.')[-1].lower()
        if file_extension not in allowed_extensions:
            raise serializers.ValidationError(f"File type not supported. Allowed: {allowed_extensions}")
        
        return value


class BatchPredictionSerializer(serializers.Serializer):
    """Serializer for batch prediction requests"""
    domain = serializers.CharField(max_length=100)
    input_type = serializers.CharField(max_length=50)
    files = serializers.ListField(
        child=serializers.FileField(),
        min_length=1,
        max_length=10
    )
    metadata = serializers.JSONField(required=False, default=dict)
    
    def validate_files(self, value):
        # Check total size
        total_size = sum(file.size for file in value)
        if total_size > 100 * 1024 * 1024:  # 100MB total limit
            raise serializers.ValidationError("Total file size cannot exceed 100MB")
        
        # Check individual file sizes and types
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.nii', '.nii.gz', '.csv', '.json']
        for file in value:
            if file.size > 50 * 1024 * 1024:
                raise serializers.ValidationError(f"File {file.name} exceeds 50MB limit")
            
            file_extension = '.' + file.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise serializers.ValidationError(f"File {file.name} has unsupported type")
        
        return value


class PredictionStatusSerializer(serializers.Serializer):
    """Serializer for prediction status responses"""
    session_id = serializers.CharField()
    status = serializers.CharField()
    progress = serializers.DictField()
    estimated_completion = serializers.DateTimeField(required=False)
    results = serializers.DictField(required=False)
