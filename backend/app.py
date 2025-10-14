from flask import Flask, request, jsonify
import numpy as np
from PIL import Image
import io

# For a real model, you would uncomment these lines and install the necessary packages
# import tensorflow as tf

app = Flask(__name__)

# --- In a real-world scenario, you would load your model here ---
# This is a placeholder. Replace it with your actual model loading logic.
# For example:
# model = tf.keras.applications.MobileNetV2(weights='imagenet')
print("Model loaded (placeholder). Ready to make predictions!")

@app.route("/")
def index():
    return "<h1>DeepMed Backend Server</h1><p>Use the /predict endpoint to make predictions.</p>"

@app.route('/predict', methods=['POST'])
def predict():
    """
    Receives an image file in a POST request and returns a JSON prediction.
    """
    # 1. Check if an image was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file:
        try:
            # 2. Read and preprocess the image
            image_bytes = file.read()
            # For a real model, you would preprocess the image to match the model's input requirements
            # For example:
            # image = Image.open(io.BytesIO(image_bytes))
            # image = image.resize((224, 224)) # MobileNetV2 expects 224x224
            # image_array = np.array(image)
            # image_array = np.expand_dims(image_array, axis=0)
            # image_array = tf.keras.applications.mobilenet_v2.preprocess_input(image_array)

            print(f"Received image: {file.filename}")

            # 3. --- Make a prediction ---
            # This is where you would call your model.
            # predictions = model.predict(image_array)
            # decoded_predictions = tf.keras.applications.imagenet_utils.decode_predictions(predictions, top=3)[0]
            
            # --- For now, we return a DUMMY response ---
            # This simulates the output for multiple models as per your project plan.
            dummy_response = {
                "aggregate_result": "2 out of 3 models predicted positive.",
                "model_predictions": [
                    {
                        "model_name": "CancerNet-A",
                        "prediction": "Positive",
                        "confidence": 0.92,
                        "paper_url": "https://example.com/paper/1"
                    },
                    {
                        "model_name": "TumorResNet-B",
                        "prediction": "Negative",
                        "confidence": 0.88,
                        "paper_url": "https://example.com/paper/2"
                    },
                    {
                        "model_name": "AlzheimerNet-C",
                        "prediction": "Positive",
                        "confidence": 0.95,
                        "paper_url": "https://example.com/paper/3"
                    }
                ]
            }

            # 4. Return the results as JSON
            return jsonify(dummy_response)

        except Exception as e:
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    # Runs the Flask app locally on port 5000
    app.run(debug=True, host='0.0.0.0')
