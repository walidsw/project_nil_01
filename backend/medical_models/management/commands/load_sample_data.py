from django.core.management.base import BaseCommand
from medical_models.models import MedicalDomain, InputType, ResearchPaper, MedicalModel, ModelCategory


class Command(BaseCommand):
    help = 'Load sample medical models and data'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample data...')
        
        # Create medical domains
        domains_data = [
            {'name': 'Cancer', 'description': 'Cancer detection and classification models'},
            {'name': 'Tumor', 'description': 'Tumor detection and analysis models'},
            {'name': 'Alzheimer\'s', 'description': 'Alzheimer\'s disease detection models'},
            {'name': 'Cardiology', 'description': 'Cardiovascular disease detection models'},
            {'name': 'Radiology', 'description': 'General radiology and imaging models'},
        ]
        
        domains = {}
        for domain_data in domains_data:
            domain, created = MedicalDomain.objects.get_or_create(
                name=domain_data['name'],
                defaults={'description': domain_data['description']}
            )
            domains[domain_data['name']] = domain
            if created:
                self.stdout.write(f'Created domain: {domain.name}')
        
        # Create input types
        input_types_data = [
            {'name': 'MRI', 'description': 'Magnetic Resonance Imaging', 'file_extension': '.nii', 'is_image': True},
            {'name': 'X-ray', 'description': 'X-ray images', 'file_extension': '.jpg', 'is_image': True},
            {'name': 'CT', 'description': 'Computed Tomography', 'file_extension': '.dcm', 'is_image': True},
            {'name': 'Tabular', 'description': 'Structured tabular data', 'file_extension': '.csv', 'is_structured': True},
            {'name': 'Text', 'description': 'Text-based medical data', 'file_extension': '.txt', 'is_structured': True},
        ]
        
        input_types = {}
        for input_type_data in input_types_data:
            input_type, created = InputType.objects.get_or_create(
                name=input_type_data['name'],
                defaults=input_type_data
            )
            input_types[input_type_data['name']] = input_type
            if created:
                self.stdout.write(f'Created input type: {input_type.name}')
        
        # Create research papers
        papers_data = [
            {
                'title': 'Deep Learning for Brain Tumor Classification',
                'authors': 'Smith, J., Johnson, A., Brown, M.',
                'journal': 'Nature Medicine',
                'year': 2023,
                'doi': '10.1038/s41591-023-01234-5',
                'url': 'https://www.nature.com/articles/s41591-023-01234-5',
                'abstract': 'A comprehensive study on using deep learning for brain tumor classification from MRI images.'
            },
            {
                'title': 'CNN-based Lung Cancer Detection from CT Scans',
                'authors': 'Chen, L., Wang, Y., Zhang, K.',
                'journal': 'IEEE Transactions on Medical Imaging',
                'year': 2023,
                'doi': '10.1109/TMI.2023.1234567',
                'url': 'https://ieeexplore.ieee.org/document/1234567',
                'abstract': 'Novel CNN architecture for early detection of lung cancer from CT scan images.'
            },
            {
                'title': 'Alzheimer\'s Disease Prediction Using Multi-modal Data',
                'authors': 'Garcia, R., Lee, S., Patel, N.',
                'journal': 'Journal of Alzheimer\'s Disease',
                'year': 2023,
                'doi': '10.3233/JAD-230123',
                'url': 'https://content.iospress.com/articles/journal-of-alzheimers-disease/jad230123',
                'abstract': 'Multi-modal approach combining MRI and clinical data for Alzheimer\'s prediction.'
            },
        ]
        
        papers = {}
        for paper_data in papers_data:
            paper, created = ResearchPaper.objects.get_or_create(
                title=paper_data['title'],
                defaults=paper_data
            )
            papers[paper_data['title']] = paper
            if created:
                self.stdout.write(f'Created research paper: {paper.title}')
        
        # Create model categories
        categories_data = [
            {'name': 'MRI-based', 'domain': 'Alzheimer\'s', 'description': 'Models using MRI images for Alzheimer\'s detection'},
            {'name': 'Data-based', 'domain': 'Alzheimer\'s', 'description': 'Models using clinical and demographic data'},
            {'name': 'Brain Tumor', 'domain': 'Tumor', 'description': 'Brain tumor detection and classification'},
            {'name': 'Lung Cancer', 'domain': 'Cancer', 'description': 'Lung cancer detection from imaging'},
        ]
        
        categories = {}
        for category_data in categories_data:
            domain = domains[category_data['domain']]
            category, created = ModelCategory.objects.get_or_create(
                name=category_data['name'],
                domain=domain,
                defaults={'description': category_data['description']}
            )
            categories[f"{category_data['domain']}_{category_data['name']}"] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create sample models
        models_data = [
            {
                'name': 'BrainTumorNet-v1',
                'description': 'CNN model for brain tumor classification from MRI images',
                'domain': 'Tumor',
                'input_type': 'MRI',
                'research_paper': 'Deep Learning for Brain Tumor Classification',
                'accuracy': 0.94,
                'precision': 0.92,
                'recall': 0.95,
                'f1_score': 0.93,
                'model_file_path': 'models/brain_tumor_net_v1.h5',
                'preprocessing_config': {
                    'target_size': [224, 224],
                    'normalize': True,
                    'augment': False
                },
                'output_classes': ['glioma', 'meningioma', 'pituitary', 'normal'],
                'framework': 'tensorflow',
                'version': '1.0'
            },
            {
                'name': 'LungCancerDetector-v2',
                'description': 'Advanced CNN for lung cancer detection from CT scans',
                'domain': 'Cancer',
                'input_type': 'CT',
                'research_paper': 'CNN-based Lung Cancer Detection from CT Scans',
                'accuracy': 0.91,
                'precision': 0.89,
                'recall': 0.93,
                'f1_score': 0.91,
                'model_file_path': 'models/lung_cancer_detector_v2.pth',
                'preprocessing_config': {
                    'target_size': [256, 256],
                    'normalize': True,
                    'augment': True
                },
                'output_classes': ['cancer', 'normal'],
                'framework': 'pytorch',
                'version': '2.0'
            },
            {
                'name': 'AlzheimerNet-MRI',
                'description': 'Multi-scale CNN for Alzheimer\'s detection from MRI',
                'domain': 'Alzheimer\'s',
                'input_type': 'MRI',
                'research_paper': 'Alzheimer\'s Disease Prediction Using Multi-modal Data',
                'accuracy': 0.88,
                'precision': 0.87,
                'recall': 0.89,
                'f1_score': 0.88,
                'model_file_path': 'models/alzheimer_net_mri.h5',
                'preprocessing_config': {
                    'target_size': [224, 224],
                    'normalize': True,
                    'augment': False
                },
                'output_classes': ['alzheimer', 'mild_cognitive_impairment', 'normal'],
                'framework': 'tensorflow',
                'version': '1.0'
            },
            {
                'name': 'AlzheimerNet-Clinical',
                'description': 'MLP model for Alzheimer\'s prediction using clinical data',
                'domain': 'Alzheimer\'s',
                'input_type': 'Tabular',
                'research_paper': 'Alzheimer\'s Disease Prediction Using Multi-modal Data',
                'accuracy': 0.82,
                'precision': 0.81,
                'recall': 0.83,
                'f1_score': 0.82,
                'model_file_path': 'models/alzheimer_net_clinical.pkl',
                'preprocessing_config': {
                    'feature_columns': ['age', 'education', 'mmse', 'cdr'],
                    'scale': True,
                    'default_values': {'age': 70, 'education': 12, 'mmse': 25, 'cdr': 0}
                },
                'output_classes': ['alzheimer', 'normal'],
                'framework': 'sklearn',
                'version': '1.0'
            },
        ]
        
        for model_data in models_data:
            domain = domains[model_data['domain']]
            input_type = input_types[model_data['input_type']]
            research_paper = papers.get(model_data['research_paper'])
            
            model, created = MedicalModel.objects.get_or_create(
                name=model_data['name'],
                version=model_data['version'],
                defaults={
                    'description': model_data['description'],
                    'domain': domain,
                    'input_type': input_type,
                    'research_paper': research_paper,
                    'accuracy': model_data['accuracy'],
                    'precision': model_data['precision'],
                    'recall': model_data['recall'],
                    'f1_score': model_data['f1_score'],
                    'model_file_path': model_data['model_file_path'],
                    'preprocessing_config': model_data['preprocessing_config'],
                    'output_classes': model_data['output_classes'],
                    'framework': model_data['framework'],
                }
            )
            
            if created:
                self.stdout.write(f'Created model: {model.name}')
                
                # Add to appropriate category
                category_key = f"{model_data['domain']}_{model_data['input_type']}"
                if category_key in categories:
                    categories[category_key].models.add(model)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample data!')
        )
