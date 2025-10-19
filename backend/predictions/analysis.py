"""
Comparative analysis engine for multiple model predictions
"""
import random
from collections import Counter
from typing import List, Dict, Any
from .models import ModelPrediction

# Mock numpy functionality
class MockNumpy:
    @staticmethod
    def mean(data):
        if isinstance(data, list):
            return sum(data) / len(data)
        return data
    
    @staticmethod
    def std(data):
        if isinstance(data, list):
            mean_val = sum(data) / len(data)
            variance = sum((x - mean_val) ** 2 for x in data) / len(data)
            return variance ** 0.5
        return 0.0
    
    @staticmethod
    def sqrt(value):
        return value ** 0.5
    
    @staticmethod
    def argmax(data):
        if isinstance(data, list):
            return data.index(max(data))
        return 0
    
    @staticmethod
    def exp(value):
        return 2.718281828459045 ** value
    
    @staticmethod
    def sign(value):
        return 1 if value >= 0 else -1

# Use mock numpy
np = MockNumpy()


class ComparativeAnalyzer:
    """Analyzes and compares predictions from multiple models"""
    
    def analyze_predictions(self, predictions: List[ModelPrediction]) -> Dict[str, Any]:
        """Perform comprehensive comparative analysis"""
        if not predictions:
            return {}
        
        # Extract prediction data
        prediction_data = []
        for pred in predictions:
            if pred.detailed_result:
                data = {
                    'model_name': pred.model.name,
                    'model_id': pred.model.id,
                    'predicted_class': pred.detailed_result.predicted_class,
                    'confidence': pred.confidence_score,
                    'class_probabilities': pred.detailed_result.class_probabilities,
                    'processing_time': pred.processing_time,
                    'accuracy': pred.model.accuracy,
                }
                prediction_data.append(data)
        
        if not prediction_data:
            return {}
        
        # Perform various analyses
        analysis = {
            'majority_vote': self._calculate_majority_vote(prediction_data),
            'weighted_average': self._calculate_weighted_average(prediction_data),
            'consensus_score': self._calculate_consensus_score(prediction_data),
            'agreement_matrix': self._calculate_agreement_matrix(prediction_data),
            'disagreement_analysis': self._analyze_disagreements(prediction_data),
            'confidence_intervals': self._calculate_confidence_intervals(prediction_data),
            'statistical_significance': self._calculate_statistical_significance(prediction_data),
            'model_performance': self._analyze_model_performance(prediction_data),
        }
        
        return analysis
    
    def _calculate_majority_vote(self, prediction_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate majority vote across all models"""
        predicted_classes = [pred['predicted_class'] for pred in prediction_data]
        class_counts = Counter(predicted_classes)
        
        most_common = class_counts.most_common(1)[0]
        total_predictions = len(predicted_classes)
        
        return {
            'predicted_class': most_common[0],
            'vote_count': most_common[1],
            'vote_percentage': (most_common[1] / total_predictions) * 100,
            'all_votes': dict(class_counts),
            'total_models': total_predictions
        }
    
    def _calculate_weighted_average(self, prediction_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate weighted average based on model accuracy and confidence"""
        # Get all unique classes
        all_classes = set()
        for pred in prediction_data:
            all_classes.update(pred['class_probabilities'].keys())
        
        weighted_probabilities = {}
        total_weight = 0
        
        for pred in prediction_data:
            # Weight based on model accuracy and prediction confidence
            model_accuracy = pred.get('accuracy', 0.5)  # Default to 0.5 if not available
            confidence = pred.get('confidence', 0.5)
            weight = model_accuracy * confidence
            total_weight += weight
            
            for class_name, probability in pred['class_probabilities'].items():
                if class_name not in weighted_probabilities:
                    weighted_probabilities[class_name] = 0
                weighted_probabilities[class_name] += probability * weight
        
        # Normalize probabilities
        if total_weight > 0:
            for class_name in weighted_probabilities:
                weighted_probabilities[class_name] /= total_weight
        
        # Find predicted class
        predicted_class = max(weighted_probabilities.items(), key=lambda x: x[1])
        
        return {
            'predicted_class': predicted_class[0],
            'confidence': predicted_class[1],
            'class_probabilities': weighted_probabilities,
            'total_weight': total_weight
        }
    
    def _calculate_consensus_score(self, prediction_data: List[Dict[str, Any]]) -> float:
        """Calculate overall consensus score (0-1)"""
        if len(prediction_data) <= 1:
            return 1.0
        
        # Calculate pairwise agreement
        agreements = 0
        total_pairs = 0
        
        for i in range(len(prediction_data)):
            for j in range(i + 1, len(prediction_data)):
                if prediction_data[i]['predicted_class'] == prediction_data[j]['predicted_class']:
                    agreements += 1
                total_pairs += 1
        
        return agreements / total_pairs if total_pairs > 0 else 0.0
    
    def _calculate_agreement_matrix(self, prediction_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate agreement matrix between models"""
        model_names = [pred['model_name'] for pred in prediction_data]
        n_models = len(model_names)
        
        # Initialize agreement matrix
        agreement_matrix = {}
        for i, model1 in enumerate(model_names):
            agreement_matrix[model1] = {}
            for j, model2 in enumerate(model_names):
                if i == j:
                    agreement_matrix[model1][model2] = 1.0
                else:
                    # Check if predictions agree
                    pred1 = prediction_data[i]['predicted_class']
                    pred2 = prediction_data[j]['predicted_class']
                    agreement_matrix[model1][model2] = 1.0 if pred1 == pred2 else 0.0
        
        return agreement_matrix
    
    def _analyze_disagreements(self, prediction_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze disagreements between models"""
        predicted_classes = [pred['predicted_class'] for pred in prediction_data]
        class_counts = Counter(predicted_classes)
        
        # Find disagreements
        disagreements = []
        for i, pred1 in enumerate(prediction_data):
            for j, pred2 in enumerate(prediction_data):
                if i < j and pred1['predicted_class'] != pred2['predicted_class']:
                    disagreements.append({
                        'model1': pred1['model_name'],
                        'model2': pred2['model_name'],
                        'prediction1': pred1['predicted_class'],
                        'prediction2': pred2['predicted_class'],
                        'confidence1': pred1['confidence'],
                        'confidence2': pred2['confidence'],
                        'confidence_diff': abs(pred1['confidence'] - pred2['confidence'])
                    })
        
        return {
            'total_disagreements': len(disagreements),
            'disagreement_rate': len(disagreements) / (len(prediction_data) * (len(prediction_data) - 1) / 2),
            'disagreements': disagreements,
            'class_distribution': dict(class_counts)
        }
    
    def _calculate_confidence_intervals(self, prediction_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate confidence intervals for predictions"""
        confidences = [pred['confidence'] for pred in prediction_data]
        
        if not confidences:
            return {}
        
        mean_confidence = np.mean(confidences)
        std_confidence = np.std(confidences)
        
        # 95% confidence interval
        ci_95 = 1.96 * std_confidence / np.sqrt(len(confidences))
        
        return {
            'mean_confidence': mean_confidence,
            'std_confidence': std_confidence,
            'confidence_interval_95': {
                'lower': max(0, mean_confidence - ci_95),
                'upper': min(1, mean_confidence + ci_95)
            },
            'min_confidence': min(confidences),
            'max_confidence': max(confidences)
        }
    
    def _calculate_statistical_significance(self, prediction_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistical significance of predictions"""
        # This is a simplified version - in practice, you might want more sophisticated tests
        
        confidences = [pred['confidence'] for pred in prediction_data]
        predicted_classes = [pred['predicted_class'] for pred in prediction_data]
        
        # Calculate p-value for majority vote (simplified)
        class_counts = Counter(predicted_classes)
        most_common_count = class_counts.most_common(1)[0][1]
        total_count = len(predicted_classes)
        
        # Binomial test approximation
        p_value = 2 * (1 - self._binomial_cdf(most_common_count - 1, total_count, 0.5))
        
        return {
            'majority_vote_p_value': p_value,
            'is_significant': p_value < 0.05,
            'effect_size': (most_common_count / total_count) - 0.5,
            'sample_size': total_count
        }
    
    def _analyze_model_performance(self, prediction_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze individual model performance in this prediction"""
        performance_data = []
        
        for pred in prediction_data:
            performance_data.append({
                'model_name': pred['model_name'],
                'model_id': pred['model_id'],
                'confidence': pred['confidence'],
                'processing_time': pred['processing_time'],
                'model_accuracy': pred['accuracy'],
                'predicted_class': pred['predicted_class']
            })
        
        # Sort by confidence
        performance_data.sort(key=lambda x: x['confidence'], reverse=True)
        
        return {
            'models_by_confidence': performance_data,
            'fastest_model': min(performance_data, key=lambda x: x['processing_time'] or float('inf')),
            'most_confident_model': max(performance_data, key=lambda x: x['confidence']),
            'highest_accuracy_model': max(performance_data, key=lambda x: x['model_accuracy'] or 0)
        }
    
    def _binomial_cdf(self, k: int, n: int, p: float) -> float:
        """Cumulative distribution function for binomial distribution (simplified)"""
        # This is a simplified implementation
        # In practice, you'd want to use scipy.stats.binom.cdf
        if k < 0:
            return 0.0
        if k >= n:
            return 1.0
        
        # Approximation using normal distribution
        mean = n * p
        std = np.sqrt(n * p * (1 - p))
        if std == 0:
            return 1.0 if k >= mean else 0.0
        
        z = (k - mean) / std
        # Simple normal CDF approximation
        return 0.5 * (1 + np.sign(z) * np.sqrt(1 - np.exp(-2 * z**2 / np.pi)))
