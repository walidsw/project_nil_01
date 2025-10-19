#!/bin/bash

# DeepMed Backend Startup Script

echo "Starting DeepMed Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing basic dependencies..."
pip install -r requirements-basic.txt

echo "Installing ML dependencies (this may take a while)..."
pip install -r requirements-ml.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp env.example .env
    echo "Please edit .env file with your configuration before running again."
    exit 1
fi

# Check if database exists
echo "Setting up database..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser (if needed)..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@deepmed.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Load sample data
echo "Loading sample data..."
python manage.py load_sample_data

# Create necessary directories
echo "Creating directories..."
mkdir -p media/uploads
mkdir -p media/models
mkdir -p logs
mkdir -p staticfiles

echo "Backend setup complete!"
echo ""
echo "To start the server:"
echo "1. Start Redis: redis-server"
echo "2. Start Celery worker: celery -A deepmed_backend worker --loglevel=info"
echo "3. Start Django server: python manage.py runserver"
echo ""
echo "Admin panel: http://localhost:8000/admin (admin/admin123)"
echo "API: http://localhost:8000/api/v1/"
