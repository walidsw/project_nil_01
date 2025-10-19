"""
API Usage Examples for DeepMed Backend

This file contains examples of how to use the DeepMed API endpoints.
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1"

def example_get_domains():
    """Get all available medical domains"""
    response = requests.get(f"{BASE_URL}/domains/")
    if response.status_code == 200:
        domains = response.json()
        print("Available domains:")
        for domain in domains:
            print(f"- {domain['name']}: {domain['description']}")
    else:
        print(f"Error: {response.status_code}")

def example_get_models():
    """Get all available models"""
    response = requests.get(f"{BASE_URL}/models/")
    if response.status_code == 200:
        models = response.json()
        print("Available models:")
        for model in models:
            print(f"- {model['name']} ({model['domain_name']})")
            print(f"  Accuracy: {model['accuracy']}")
            print(f"  Framework: {model['framework']}")
    else:
        print(f"Error: {response.status_code}")

def example_compare_models():
    """Get models for comparison in a specific domain"""
    data = {
        "domain_id": 1,  # Cancer domain
        "input_type_id": 1  # MRI input type
    }
    
    response = requests.post(f"{BASE_URL}/models/compare_models/", json=data)
    if response.status_code == 200:
        result = response.json()
        print(f"Found {result['count']} models for comparison:")
        for model in result['models']:
            print(f"- {model['name']}")
    else:
        print(f"Error: {response.status_code}")

def example_upload_and_predict():
    """Upload a file and start prediction"""
    # This would typically be a real medical image file
    files = {
        'file': ('sample_mri.jpg', open('sample_mri.jpg', 'rb'), 'image/jpeg')
    }
    
    data = {
        'domain': 'Tumor',
        'input_type': 'MRI',
        'metadata': json.dumps({
            'patient_age': 45,
            'scan_type': 'T1-weighted'
        })
    }
    
    response = requests.post(f"{BASE_URL}/sessions/upload_and_predict/", files=files, data=data)
    if response.status_code == 201:
        result = response.json()
        session_id = result['session_id']
        print(f"Prediction started! Session ID: {session_id}")
        return session_id
    else:
        print(f"Error: {response.status_code}")
        return None

def example_check_prediction_status(session_id):
    """Check the status of a prediction session"""
    response = requests.get(f"{BASE_URL}/status/{session_id}/")
    if response.status_code == 200:
        status = response.json()
        print(f"Session Status: {status['status']}")
        print(f"Progress: {status['progress']['percentage']:.1f}%")
        
        if status['status'] == 'completed':
            print("Prediction completed!")
            return True
        else:
            print("Prediction still processing...")
            return False
    else:
        print(f"Error: {response.status_code}")
        return False

def example_get_prediction_results(session_id):
    """Get detailed prediction results"""
    response = requests.get(f"{BASE_URL}/sessions/{session_id}/results/")
    if response.status_code == 200:
        results = response.json()
        print("Prediction Results:")
        print(f"Domain: {results['domain']}")
        print(f"Input Type: {results['input_type']}")
        print(f"Consensus Score: {results['consensus_score']}")
        
        print("\nIndividual Model Results:")
        for result in results['individual_results']:
            print(f"- {result['model']['name']}:")
            print(f"  Predicted Class: {result['prediction']['predicted_class']}")
            print(f"  Confidence: {result['prediction']['confidence']:.3f}")
            print(f"  Processing Time: {result['prediction']['processing_time']:.2f}s")
        
        print("\nComparative Analysis:")
        analysis = results['comparative_analysis']
        if analysis:
            print(f"Majority Vote: {analysis['majority_vote']['predicted_class']}")
            print(f"Vote Percentage: {analysis['majority_vote']['vote_percentage']:.1f}%")
            print(f"Consensus Score: {analysis['consensus_score']:.3f}")
    else:
        print(f"Error: {response.status_code}")

def example_batch_prediction():
    """Upload multiple files for batch prediction"""
    files = []
    for i in range(3):
        files.append(('files', (f'sample_{i}.jpg', open(f'sample_{i}.jpg', 'rb'), 'image/jpeg')))
    
    data = {
        'domain': 'Cancer',
        'input_type': 'X-ray',
        'metadata': json.dumps({'batch_id': 'batch_001'})
    }
    
    response = requests.post(f"{BASE_URL}/sessions/batch_predict/", files=files, data=data)
    if response.status_code == 201:
        result = response.json()
        print(f"Batch prediction started for {result['count']} files")
        print(f"Session IDs: {result['session_ids']}")
        return result['session_ids']
    else:
        print(f"Error: {response.status_code}")
        return []

def example_get_user_stats():
    """Get user statistics (requires authentication)"""
    # First, get authentication token
    auth_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    response = requests.post(f"{BASE_URL}/auth/token/", data=auth_data)
    if response.status_code == 200:
        token = response.json()['token']
        headers = {'Authorization': f'Token {token}'}
        
        # Get user stats
        response = requests.get(f"{BASE_URL}/users/stats/", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print("User Statistics:")
            print(f"Total Sessions: {stats['total_prediction_sessions']}")
            print(f"Completed Sessions: {stats['completed_sessions']}")
            print(f"Success Rate: {stats['success_rate']:.1f}%")
        else:
            print(f"Error: {response.status_code}")
    else:
        print("Authentication failed")

def main():
    """Run all examples"""
    print("DeepMed API Examples")
    print("=" * 50)
    
    # Basic API calls
    print("\n1. Getting available domains...")
    example_get_domains()
    
    print("\n2. Getting available models...")
    example_get_models()
    
    print("\n3. Comparing models...")
    example_compare_models()
    
    # Prediction workflow
    print("\n4. Starting prediction...")
    session_id = example_upload_and_predict()
    
    if session_id:
        print("\n5. Checking prediction status...")
        # In a real scenario, you would poll this endpoint
        # until the prediction is completed
        example_check_prediction_status(session_id)
        
        print("\n6. Getting prediction results...")
        example_get_prediction_results(session_id)
    
    # Batch prediction
    print("\n7. Batch prediction...")
    example_batch_prediction()
    
    # User stats
    print("\n8. User statistics...")
    example_get_user_stats()

if __name__ == "__main__":
    main()
