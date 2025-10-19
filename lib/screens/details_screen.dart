import 'package:flutter/material.dart';
import 'dart:io';
import 'package:url_launcher/url_launcher.dart';

class ModelPrediction {
  final String modelName;
  final String description;
  final String prediction;
  final double confidence;
  final String paperUrl;

  ModelPrediction({
    required this.modelName,
    required this.description,
    required this.prediction,
    required this.confidence,
    required this.paperUrl,
  });
}

class DetailsScreen extends StatelessWidget {
  final List<ModelPrediction> predictions;
  final File imageFile;
  final String diseaseType;

  const DetailsScreen({
    super.key,
    required this.predictions,
    required this.imageFile,
    required this.diseaseType,
  });

  Future<void> _launchURL(String url) async {
    final Uri uri = Uri.parse(url);
    if (!await launchUrl(uri, mode: LaunchMode.externalApplication)) {
      debugPrint('Could not launch $url');
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text("Detailed Model Results"),
        centerTitle: false,
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16.0),
        itemCount: predictions.length,
        itemBuilder: (context, index) {
          final prediction = predictions[index];
          final isPositive = prediction.prediction.toLowerCase() == 'positive';
          final resultColor = isPositive ? Colors.red.shade700 : Colors.green.shade700;

          return Card(
            margin: const EdgeInsets.only(bottom: 16),
            elevation: 2,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
              side: BorderSide(color: resultColor.withValues(alpha: 0.3), width: 1),
            ),
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Model Name
                  Row(
                    children: [
                      Icon(Icons.model_training, color: theme.primaryColor, size: 20),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          prediction.modelName,
                          style: theme.textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),

                  // Description
                  Text(
                    prediction.description,
                    style: theme.textTheme.bodySmall?.copyWith(
                      color: Colors.grey.shade600,
                    ),
                  ),
                  const SizedBox(height: 16),

                  // Prediction Result
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: resultColor.withValues(alpha: 0.1),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: resultColor.withValues(alpha: 0.3)),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              "Prediction",
                              style: TextStyle(
                                fontSize: 12,
                                color: Colors.grey.shade600,
                              ),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              prediction.prediction,
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                                color: resultColor,
                              ),
                            ),
                          ],
                        ),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.end,
                          children: [
                            Text(
                              "Confidence",
                              style: TextStyle(
                                fontSize: 12,
                                color: Colors.grey.shade600,
                              ),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              "${(prediction.confidence * 100).toStringAsFixed(1)}%",
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                                color: resultColor,
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 12),

                  // View Paper Button
                  TextButton.icon(
                    onPressed: () => _launchURL(prediction.paperUrl),
                    icon: const Icon(Icons.description_outlined, size: 18),
                    label: const Text("View Research Paper"),
                    style: TextButton.styleFrom(
                      foregroundColor: theme.primaryColor,
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}