from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class MedicalDomain(models.Model):
    """Represents different medical domains (Cancer, Tumor, Alzheimer's, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class InputType(models.Model):
    """Represents different input types (MRI, Tabular, Text, etc.)"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    file_extension = models.CharField(max_length=10, blank=True)
    is_image = models.BooleanField(default=False)
    is_structured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ResearchPaper(models.Model):
    """Represents research papers associated with models"""
    title = models.CharField(max_length=500)
    authors = models.TextField()
    journal = models.CharField(max_length=200, blank=True)
    year = models.IntegerField()
    doi = models.CharField(max_length=100, blank=True)
    arxiv_id = models.CharField(max_length=50, blank=True)
    url = models.URLField(blank=True)
    abstract = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year', 'title']

    def __str__(self):
        return f"{self.title} ({self.year})"


class MedicalModel(models.Model):
    """Represents a medical ML model"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Under Maintenance'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    domain = models.ForeignKey(MedicalDomain, on_delete=models.CASCADE, related_name='models')
    input_type = models.ForeignKey(InputType, on_delete=models.CASCADE, related_name='models')
    research_paper = models.ForeignKey(ResearchPaper, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Model metadata
    accuracy = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        null=True, blank=True
    )
    precision = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        null=True, blank=True
    )
    recall = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        null=True, blank=True
    )
    f1_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        null=True, blank=True
    )
    
    # Model files and configuration
    model_file_path = models.CharField(max_length=500)
    preprocessing_config = models.JSONField(default=dict, blank=True)
    output_classes = models.JSONField(default=list, blank=True)
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    version = models.CharField(max_length=20, default='1.0')
    framework = models.CharField(max_length=50, default='tensorflow')  # tensorflow, pytorch, onnx
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['name', 'version']

    def __str__(self):
        return f"{self.name} v{self.version}"

    @property
    def is_available(self):
        return self.status == 'active'

    def get_model_info(self):
        """Return model information for API responses"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'domain': self.domain.name,
            'input_type': self.input_type.name,
            'accuracy': self.accuracy,
            'precision': self.precision,
            'recall': self.recall,
            'f1_score': self.f1_score,
            'status': self.status,
            'version': self.version,
            'framework': self.framework,
            'output_classes': self.output_classes,
            'research_paper': {
                'title': self.research_paper.title,
                'authors': self.research_paper.authors,
                'year': self.research_paper.year,
                'doi': self.research_paper.doi,
                'url': self.research_paper.url,
            } if self.research_paper else None,
        }


class ModelCategory(models.Model):
    """Represents categories within domains (e.g., MRI-based, Data-based for Alzheimer's)"""
    name = models.CharField(max_length=100)
    domain = models.ForeignKey(MedicalDomain, on_delete=models.CASCADE, related_name='categories')
    description = models.TextField(blank=True)
    models = models.ManyToManyField(MedicalModel, related_name='categories', blank=True)

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'domain']

    def __str__(self):
        return f"{self.domain.name} - {self.name}"
