import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

// --- Data Structures for Results ---

/// Represents the result from a single ML model.
class SingleModelResult {
  final String modelName;
  final String prediction;
  final double confidence;
  final String paperUrl; // Link to the model's research paper

  SingleModelResult({
    required this.modelName,
    required this.prediction,
    required this.confidence,
    required this.paperUrl,
  });
}

/// Represents the combined analysis from multiple models.
class MultiModelAnalysisResult {
  final String overallPrediction;
  final double averageConfidence;
  final List<SingleModelResult> individualResults;

  MultiModelAnalysisResult({
    required this.overallPrediction,
    required this.averageConfidence,
    required this.individualResults,
  });
}


class MultiModelResultScreen extends StatelessWidget {
  final MultiModelAnalysisResult analysisResult;

  const MultiModelResultScreen({super.key, required this.analysisResult});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Analysis Report"),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16.0),
        children: [
          _buildAverageResultHeader(context),
          const SizedBox(height: 24),
          Text(
            "Individual Model Results",
            style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 16),
          ...analysisResult.individualResults.map((result) => _buildResultCard(context, result)),
        ],
      ),
    );
  }

  Widget _buildAverageResultHeader(BuildContext context) {
    return Card(
      elevation: 4,
      color: Theme.of(context).primaryColor,
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const Text(
              "Average Result",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white),
            ),
            const SizedBox(height: 16),
            Text(
              analysisResult.overallPrediction,
              style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Colors.white),
            ),
            const SizedBox(height: 8),
            Text(
              "Based on ${analysisResult.individualResults.length} models",
              style: TextStyle(color: Colors.white.withOpacity(0.8)),
            ),
            const SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.shield_moon, color: Colors.white70),
                const SizedBox(width: 8),
                Text(
                  "Avg. Confidence: ${(analysisResult.averageConfidence * 100).toStringAsFixed(1)}%",
                  style: const TextStyle(fontSize: 16, color: Colors.white),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildResultCard(BuildContext context, SingleModelResult result) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              result.modelName,
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const Divider(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text("Prediction:", style: TextStyle(color: Colors.grey)),
                Text(result.prediction, style: const TextStyle(fontWeight: FontWeight.bold)),
              ],
            ),
            const SizedBox(height: 8),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text("Confidence:", style: TextStyle(color: Colors.grey)),
                Text(
                  "${(result.confidence * 100).toStringAsFixed(1)}%",
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Align(
              alignment: Alignment.centerRight,
              child: TextButton.icon(
                icon: const Icon(Icons.article_outlined, size: 18),
                label: const Text("Read Paper"),
                onPressed: () async {
                  final url = Uri.parse(result.paperUrl);
                  if (await canLaunchUrl(url)) {
                    await launchUrl(url);
                  }
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}