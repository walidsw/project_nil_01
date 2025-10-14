import 'package:flutter/material.dart';
import 'dart:io';

class ResultScreen extends StatelessWidget {
  final String modelName;
  final File imageFile;
  final String modelResult; // e.g., "Malignant (94.5% Confidence)"

  const ResultScreen({
    super.key,
    required this.modelName,
    required this.imageFile,
    required this.modelResult,
  });

  // Helper to determine the color of the result banner based on the prediction
  Color _getResultColor(BuildContext context, String result) {
    if (result.toLowerCase().contains('malignant') || result.toLowerCase().contains('tumor') || result.toLowerCase().contains('positive')) {
      // Use a warning or danger color for critical results (red)
      return Colors.red.shade700;
    }
    // Use the secondary (success) color for benign or neutral results (green/blue)
    return Theme.of(context).colorScheme.secondary;
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final resultColor = _getResultColor(context, modelResult);

    return Scaffold(
      appBar: AppBar(
        title: const Text("Analysis Complete"),
        centerTitle: false,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // --- Model Name and Description ---
            Text(
              "Model Used: $modelName",
              style: theme.textTheme.titleMedium?.copyWith(
                color: Colors.grey.shade600,
              ),
            ),
            const SizedBox(height: 8),

            // --- Prediction Result Card (Highlight) ---
            Card(
              color: resultColor.withOpacity(0.1),
              elevation: 0,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(16),
                side: BorderSide(color: resultColor, width: 2),
              ),
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  children: [
                    Text(
                      "Prediction Result",
                      style: theme.textTheme.titleLarge?.copyWith(color: resultColor),
                    ),
                    const SizedBox(height: 12),
                    Text(
                      modelResult,
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 36,
                        fontWeight: FontWeight.w900,
                        color: resultColor,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      "Disclaimer: This result is for research purposes only and is not a substitute for professional medical advice.",
                      textAlign: TextAlign.center,
                      style: TextStyle(fontSize: 12, color: resultColor.withOpacity(0.8)),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 32),

            // --- Input Image Preview ---
            Text(
              "Analyzed Input Image",
              style: theme.textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            Container(
              height: 300,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.grey.shade300, width: 1),
                color: Colors.grey.shade50,
              ),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: Image.file(
                  imageFile,
                  fit: BoxFit.cover,
                ),
              ),
            ),
            const SizedBox(height: 32),

            // --- Action Buttons ---
            ElevatedButton.icon(
              onPressed: () {
                // Placeholder for linking to the original paper
                debugPrint("Viewing research paper for $modelName");
              },
              icon: const Icon(Icons.description),
              label: const Text("View Original Research Paper"),
              style: ElevatedButton.styleFrom(
                backgroundColor: theme.primaryColor,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 14),
              ),
            ),
            const SizedBox(height: 12),
            OutlinedButton.icon(
              onPressed: () => Navigator.popUntil(context, (route) => route.isFirst),
              icon: const Icon(Icons.home_outlined),
              label: const Text("Return to Home"),
              style: OutlinedButton.styleFrom(
                foregroundColor: theme.primaryColor,
                side: BorderSide(color: theme.primaryColor),
                padding: const EdgeInsets.symmetric(vertical: 14),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
