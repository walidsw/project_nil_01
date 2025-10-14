from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import os

from config.config import config
from models.model_manager import ModelManager
from utils.validators import allowed_file, validate_image
from utils.image_processor import ImageProcessor

def create_app(config_name='development'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Initialize model manager
    model_manager = ModelManager(app.config['MODEL_PATH'])
    image_processor = ImageProcessor()
    
    @app.route("/")
    def index():
        return jsonify({
            "name": "DeepMed Backend Server",
            "version": "1.0.0",
            "status": "running",
            "endpoints": {
                "predict": "/predict",
                "health": "/health",
                "models": "/models"
            }
        })
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "models_loaded": len(model_manager.models),
            "ready": True
        }), 200
    
    @app.route('/models', methods=['GET'])
    def list_models():
        """List all available models"""
        models_info = []
        for name, info in model_manager.models.items():
            models_info.append({
                "name": name,
                "description": info['description'],
                "paper_url": info['paper_url']
            })
        
        return jsonify({
            "total_models": len(models_info),
            "models": models_info
        }), 200
    
    @app.route('/predict', methods=['POST'])
    def predict():
        """
        Receives an image file in a POST request and returns predictions from multiple models.
        """
        # 1. Validate request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['file']
        
        # 2. Validate file
        is_valid, message = validate_image(file)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        try:
            # 3. Read and process image
            image_bytes = file.read()
            image = image_processor.read_image(image_bytes)
            
            # 4. Validate medical image format
            if not image_processor.validate_medical_format(image):
                return jsonify({
                    'error': 'Image does not meet minimum requirements (min 224x224)'
                }), 400
            
            # 5. Enhance image (optional for medical images)
            image = image_processor.enhance_medical_image(image)
            
            # 6. Get predictions from all models
            results = model_manager.predict(image)
            
            # 7. Add metadata
            results['metadata'] = {
                'filename': file.filename,
                'image_size': image.size,
                'format': image.format or 'Unknown'
            }
            
            return jsonify(results), 200
            
        except ValueError as ve:
            return jsonify({'error': f'Invalid image: {str(ve)}'}), 400
        except Exception as e:
            app.logger.error(f"Prediction error: {str(e)}")
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        """Handle file too large error"""
        return jsonify({
            'error': 'File too large',
            'max_size': f"{app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024)}MB"
        }), 413
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle internal server errors"""
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    # Create app with development config
    app = create_app('development')
    
    # Run the Flask app
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
