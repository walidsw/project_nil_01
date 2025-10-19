from rest_framework import serializers
from .models import MedicalDomain, InputType, ResearchPaper, MedicalModel, ModelCategory


class ResearchPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchPaper
        fields = ['id', 'title', 'authors', 'journal', 'year', 'doi', 'arxiv_id', 'url', 'abstract']


class InputTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputType
        fields = ['id', 'name', 'description', 'file_extension', 'is_image', 'is_structured']


class MedicalDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalDomain
        fields = ['id', 'name', 'description', 'created_at']


class ModelCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelCategory
        fields = ['id', 'name', 'description']


class MedicalModelSerializer(serializers.ModelSerializer):
    domain = MedicalDomainSerializer(read_only=True)
    input_type = InputTypeSerializer(read_only=True)
    research_paper = ResearchPaperSerializer(read_only=True)
    categories = ModelCategorySerializer(many=True, read_only=True)
    
    domain_id = serializers.IntegerField(write_only=True)
    input_type_id = serializers.IntegerField(write_only=True)
    research_paper_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = MedicalModel
        fields = [
            'id', 'name', 'description', 'domain', 'input_type', 'research_paper',
            'accuracy', 'precision', 'recall', 'f1_score', 'status', 'version',
            'framework', 'output_classes', 'preprocessing_config', 'created_at',
            'updated_at', 'categories', 'domain_id', 'input_type_id', 'research_paper_id'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        # Handle foreign key relationships
        domain_id = validated_data.pop('domain_id')
        input_type_id = validated_data.pop('input_type_id')
        research_paper_id = validated_data.pop('research_paper_id', None)
        
        domain = MedicalDomain.objects.get(id=domain_id)
        input_type = InputType.objects.get(id=input_type_id)
        research_paper = ResearchPaper.objects.get(id=research_paper_id) if research_paper_id else None
        
        validated_data['domain'] = domain
        validated_data['input_type'] = input_type
        validated_data['research_paper'] = research_paper
        
        return super().create(validated_data)


class MedicalModelListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    domain_name = serializers.CharField(source='domain.name', read_only=True)
    input_type_name = serializers.CharField(source='input_type.name', read_only=True)
    research_paper_title = serializers.CharField(source='research_paper.title', read_only=True)

    class Meta:
        model = MedicalModel
        fields = [
            'id', 'name', 'description', 'domain_name', 'input_type_name',
            'accuracy', 'status', 'version', 'framework', 'research_paper_title'
        ]


class ModelComparisonSerializer(serializers.Serializer):
    """Serializer for model comparison requests"""
    domain_id = serializers.IntegerField()
    input_type_id = serializers.IntegerField(required=False)
    category_id = serializers.IntegerField(required=False)
    
    def validate(self, data):
        domain_id = data.get('domain_id')
        if not MedicalDomain.objects.filter(id=domain_id).exists():
            raise serializers.ValidationError("Invalid domain ID")
        return data
