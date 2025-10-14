# DeepMed Backend

Medical ML prediction backend with multiple model support.

## Setup

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables
The `.env` file is already configured. You can modify it if needed.

### 4. Run the Server
```bash
python app.py
```

Server will start at `http://localhost:5000`

## Testing

### Test Health Check
```bash
curl http://localhost:5000/health
```

### Test List Models
```bash
curl http://localhost:5000/models
```

### Test with cURL
```bash
curl -X POST http://localhost:5000/predict \
  -F "file=@path/to/image.jpg"
```

## Project Structure
```
backend/
├── app.py                 # Main application
├── requirements.txt       # Dependencies
├── .env                   # Environment variables
├── config/
│   ├── __init__.py
│   └── config.py         # Configuration
├── models/
│   ├── __init__.py
│   └── model_manager.py  # Model management
├── utils/
│   ├── __init__.py
│   ├── validators.py     # Input validation
│   └── image_processor.py # Image processing
└── README.md             # This file
```

## API Endpoints

### GET /
Returns server information

### GET /health
Health check endpoint

### GET /models
List all available models

### POST /predict
Submit an image for prediction
- Content-Type: multipart/form-data
- Body: file (image file)