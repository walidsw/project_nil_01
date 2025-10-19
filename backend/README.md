# DeepMed Backend

A comprehensive backend system for the DeepMed medical AI platform that integrates multiple machine learning models for comparative analysis and medical diagnosis.

## Features

- **Multi-Model Integration**: Support for TensorFlow, PyTorch, and ONNX models
- **Comparative Analysis**: Run multiple models on the same input and get aggregated results
- **Medical Domains**: Organized by medical specialties (Cancer, Tumor, Alzheimer's, etc.)
- **File Processing**: Handle various medical data formats (MRI, X-ray, tabular data)
- **RESTful API**: Complete API for frontend integration
- **Background Processing**: Asynchronous prediction processing with Celery
- **User Management**: Authentication and user session tracking
- **Research Integration**: Links to original research papers and citations

## Architecture

### Core Components

1. **Medical Models App** (`medical_models/`)
   - Model metadata and configuration
   - Research paper integration
   - Domain and category management

2. **Predictions App** (`predictions/`)
   - Prediction session management
   - ML inference engine
   - Comparative analysis
   - Background task processing

3. **Users App** (`users/`)
   - User authentication and management
   - User statistics and history

### ML Engine

The ML engine supports:
- **TensorFlow/Keras models**
- **PyTorch models**
- **ONNX models** (planned)
- **Image preprocessing** (MRI, X-ray, CT, etc.)
- **Tabular data preprocessing**
- **Batch processing**

### Comparative Analysis

- **Majority voting**
- **Weighted averaging** (based on model accuracy)
- **Consensus scoring**
- **Statistical significance testing**
- **Agreement matrix analysis**

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL
- Redis
- Virtual environment

### Installation

1. **Clone and navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   # Create PostgreSQL database
   createdb deepmed_db
   
   # Run migrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load sample data** (optional)
   ```bash
   python manage.py loaddata sample_data.json
   ```

### Running the Server

1. **Start Redis** (for Celery)
   ```bash
   redis-server
   ```

2. **Start Celery worker** (in separate terminal)
   ```bash
   celery -A deepmed_backend worker --loglevel=info
   ```

3. **Start Django server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/v1/`

## API Endpoints

### Medical Models
- `GET /api/v1/domains/` - List all medical domains
- `GET /api/v1/models/` - List all available models
- `GET /api/v1/models/compare_models/` - Get models for comparison
- `GET /api/v1/categories/` - List model categories

### Predictions
- `POST /api/v1/sessions/upload_and_predict/` - Upload file and start prediction
- `POST /api/v1/sessions/batch_predict/` - Batch prediction
- `GET /api/v1/sessions/{id}/` - Get prediction session details
- `GET /api/v1/sessions/{id}/results/` - Get prediction results
- `GET /api/v1/status/{session_id}/` - Get prediction status

### Users
- `GET /api/v1/users/me/` - Get current user info
- `GET /api/v1/users/stats/` - Get user statistics
- `POST /api/v1/auth/token/` - Get authentication token

## Model Integration

### Adding New Models

1. **Prepare model files**
   - Save model in supported format (TensorFlow/PyTorch)
   - Create preprocessing configuration
   - Document input/output specifications

2. **Add to database**
   ```python
   from medical_models.models import MedicalModel, MedicalDomain, InputType
   
   # Create model entry
   model = MedicalModel.objects.create(
       name="Your Model Name",
       description="Model description",
       domain=domain,
       input_type=input_type,
       model_file_path="path/to/model",
       preprocessing_config={
           "target_size": [224, 224],
           "normalize": True,
           "augment": False
       },
       output_classes=["class1", "class2"],
       framework="tensorflow"
   )
   ```

3. **Test integration**
   ```bash
   python manage.py shell
   >>> from predictions.ml_engine import inference_engine
   >>> # Test your model
   ```

### Supported Input Types

- **MRI Images**: NIfTI, DICOM (planned)
- **General Images**: JPG, PNG, TIFF
- **Tabular Data**: CSV, JSON
- **Text Data**: JSON format

## Deployment

### Production Setup

1. **Environment variables**
   ```bash
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   ALLOWED_HOSTS=your-domain.com
   ```

2. **Static files**
   ```bash
   python manage.py collectstatic
   ```

3. **Database optimization**
   ```bash
   python manage.py migrate
   ```

4. **Use production WSGI server**
   ```bash
   gunicorn deepmed_backend.wsgi:application
   ```

### Docker Deployment (Optional)

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "deepmed_backend.wsgi:application"]
```

## Monitoring and Logging

- **Logs**: Stored in `logs/django.log`
- **Celery monitoring**: Use Flower or Celery monitoring tools
- **Database monitoring**: PostgreSQL logs and performance metrics

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Create GitHub issue
- Check documentation
- Contact development team
