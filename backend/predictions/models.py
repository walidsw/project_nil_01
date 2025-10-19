from django.db import models
from django.contrib.auth.models import User
from medical_models.models import MedicalModel


class PredictionSession(models.Model):
    """Represents a prediction session with multiple models"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True)
    domain = models.CharField(max_length=100)
    input_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Input data information
    input_file_path = models.CharField(max_length=500, blank=True)
    input_metadata = models.JSONField(default=dict, blank=True)
    
    # Results
    aggregated_result = models.JSONField(default=dict, blank=True)
    confidence_score = models.FloatField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Session {self.session_id} - {self.domain}"

    @property
    def is_completed(self):
        return self.status == 'completed'

    @property
    def is_processing(self):
        return self.status == 'processing'


class ModelPrediction(models.Model):
    """Represents individual model predictions within a session"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    session = models.ForeignKey(PredictionSession, on_delete=models.CASCADE, related_name='predictions')
    model = models.ForeignKey(MedicalModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Prediction results
    prediction_result = models.JSONField(default=dict, blank=True)
    confidence_score = models.FloatField(null=True, blank=True)
    processing_time = models.FloatField(null=True, blank=True)  # in seconds
    
    # Error information
    error_message = models.TextField(blank=True)
    error_details = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['session', 'model']

    def __str__(self):
        return f"{self.session.session_id} - {self.model.name}"

    @property
    def is_completed(self):
        return self.status == 'completed'

    @property
    def is_successful(self):
        return self.status == 'completed' and not self.error_message


class PredictionResult(models.Model):
    """Detailed prediction results for analysis"""
    prediction = models.OneToOneField(ModelPrediction, on_delete=models.CASCADE, related_name='detailed_result')
    
    # Raw model output
    raw_output = models.JSONField(default=dict, blank=True)
    
    # Processed results
    predicted_class = models.CharField(max_length=100, blank=True)
    class_probabilities = models.JSONField(default=dict, blank=True)
    
    # Additional metrics
    uncertainty_score = models.FloatField(null=True, blank=True)
    attention_weights = models.JSONField(default=dict, blank=True)  # For attention-based models
    
    # Metadata
    model_version = models.CharField(max_length=20, blank=True)
    preprocessing_applied = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.prediction}"


class ComparativeAnalysis(models.Model):
    """Stores comparative analysis results"""
    session = models.OneToOneField(PredictionSession, on_delete=models.CASCADE, related_name='comparative_analysis')
    
    # Aggregated results
    majority_vote = models.CharField(max_length=100, blank=True)
    weighted_average = models.JSONField(default=dict, blank=True)
    consensus_score = models.FloatField(null=True, blank=True)
    
    # Model agreement analysis
    agreement_matrix = models.JSONField(default=dict, blank=True)
    disagreement_analysis = models.JSONField(default=dict, blank=True)
    
    # Statistical analysis
    confidence_intervals = models.JSONField(default=dict, blank=True)
    statistical_significance = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analysis for {self.session.session_id}"
