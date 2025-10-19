#!/bin/bash

# DeepMed Backend Simple Start

echo "Starting DeepMed Backend (Simple Setup)..."

# Remove existing virtual environment if it exists
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

# Create new virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install simple dependencies
echo "Installing dependencies..."
pip install -r requirements-simple.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp env.example .env
    echo "Please edit .env file with your configuration before running again."
    exit 1
fi

# Set up database (using SQLite for simplicity)
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

echo "Simple setup complete!"
echo ""
echo "To start the server:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Start Django server: python manage.py runserver"
echo ""
echo "Admin panel: http://localhost:8000/admin (admin/admin123)"
echo "API: http://localhost:8000/api/v1/"
