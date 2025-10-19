import 'dart:io';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'multi_model_result_screen.dart'; // Import the new screen
import 'single_model_result_screen.dart'; // Add this import at the top

class UploadScreen extends StatefulWidget {
  final String modelName;
  final String modelDescription;
  final String
  modalityName; // New parameter to show input type (e.g., MRI, X-Ray)

  const UploadScreen({
    super.key,
    required this.modelName,
    required this.modelDescription,
    required this.modalityName,
  });

  @override
  State<UploadScreen> createState() => _UploadScreenState();
}

class _UploadScreenState extends State<UploadScreen> {
  XFile? _imageFile;
  bool _isAnalyzing = false; // Add state for loading indicator
  final ImagePicker _picker = ImagePicker();

  // --- Image Picking Logic ---
  Future<void> _pickImage() async {
    try {
      final pickedFile = await _picker.pickImage(
        source: ImageSource.gallery,
        imageQuality: 85,
        maxWidth: 1024,
        maxHeight: 1024,
      );
      if (pickedFile != null) {
        setState(() {
          _imageFile = pickedFile;
        });
      }
    } catch (e) {
      debugPrint('Image pick error: $e');
      if (mounted) {
        String errorMessage = 'Error selecting image';
        if (e.toString().contains('Permission')) {
          errorMessage =
              'Permission denied. Please allow photo access in Settings.';
        } else if (e.toString().contains('No photos')) {
          errorMessage = 'No photos found in gallery.';
        } else {
          errorMessage = 'Error: ${e.toString()}';
        }

        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(errorMessage),
            backgroundColor: Colors.red,
            duration: const Duration(seconds: 4),
            action: SnackBarAction(
              label: 'Settings',
              textColor: Colors.white,
              onPressed: () {
                // Could open app settings here
              },
            ),
          ),
        );
      }
    }
  }

  // --- NEW: Simulate multi-model analysis ---
  Future<void> _runMultiModelAnalysis() async {
    if (_imageFile == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please select an image first!")),
      );
      return;
    }

    setState(() => _isAnalyzing = true);

    // Simulate network delay and analysis
    await Future.delayed(const Duration(seconds: 3));

    // --- Generate Dummy Results ---
    final models = ["ResNet50", "VGG16", "InceptionV3"];
    final predictions = ["Positive", "Negative"];
    final random = Random();
    final List<SingleModelResult> individualResults = models.map((modelName) {
      return SingleModelResult(
        modelName: modelName,
        prediction: predictions[random.nextInt(predictions.length)],
        confidence: 0.85 + random.nextDouble() * 0.14, // 85% to 99%
        paperUrl: "https://arxiv.org/abs/1512.03385", // Dummy paper link
      );
    }).toList();

    // Calculate average result
    final double avgConfidence = individualResults.map((r) => r.confidence).reduce((a, b) => a + b) / individualResults.length;
    final String overallPrediction = individualResults.map((r) => r.prediction).fold<Map<String, int>>({}, (map, pred) {
      map[pred] = (map[pred] ?? 0) + 1;
      return map;
    }).entries.reduce((a, b) => a.value > b.value ? a : b).key;

    final analysisResult = MultiModelAnalysisResult(
      overallPrediction: overallPrediction,
      averageConfidence: avgConfidence,
      individualResults: individualResults,
    );
    // --- End of Dummy Data Generation ---

    setState(() => _isAnalyzing = false);

    // Navigate to the new results screen
    if (mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => MultiModelResultScreen(analysisResult: analysisResult),
        ),
      );
    }
  }

  // --- Simulate single-model analysis ---
  Future<void> _runSingleModelAnalysis() async {
    if (_imageFile == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please select an image first!")),
      );
      return;
    }
    
    setState(() => _isAnalyzing = true);
    
    // Simulate network delay and analysis
    await Future.delayed(const Duration(seconds: 2));
    
    // Generate dummy result
    final random = Random();
    final predictions = ["Positive", "Negative", "Uncertain"];
    final prediction = predictions[random.nextInt(predictions.length)];
    final confidence = 0.85 + random.nextDouble() * 0.14; // 85% to 99%
    
    setState(() => _isAnalyzing = false);
    
    // Navigate to result screen
    if (mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => SingleModelResultScreen(
            modelName: widget.modelName,
            prediction: prediction,
            confidence: confidence,
            paperUrl: "https://arxiv.org/abs/1512.03385", // Dummy paper URL
            imagePath: _imageFile!.path,
          ),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final screenHeight = MediaQuery.of(context).size.height;
    final screenWidth = MediaQuery.of(context).size.width;

    // Use a smaller portion of the screen for the image preview
    final double imageHeight = screenHeight * 0.3; 
    // Make padding responsive
    final double horizontalPadding = screenWidth > 600 ? 40.0 : 16.0;

    return Scaffold(
      appBar: AppBar(
        title: Text(widget.modelName),
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.symmetric(horizontal: horizontalPadding, vertical: 16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // --- Model Information Card ---
            Card(
              color: theme.primaryColor.withValues(
                alpha: 0.05,
              ), // Changed from withOpacity
              elevation: 0,
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "Input Required: ${widget.modalityName}",
                      style: theme.textTheme.titleMedium?.copyWith(
                        color: theme.primaryColor,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      widget.modelDescription,
                      style: TextStyle(color: Colors.grey.shade700),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // --- Image Preview Area (NOW TAPPABLE) ---
            GestureDetector(
              onTap: _pickImage, // This makes the area tappable
              child: Container(
                height: imageHeight, // Use dynamic height
                width: double.infinity,
                decoration: BoxDecoration(
                  color: Colors.grey.shade100,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.grey.shade300, width: 2),
                ),
                child: Center(
                  child: _imageFile != null
                      ? ClipRRect(
                          borderRadius: BorderRadius.circular(10),
                          child: Image.file(
                            File(_imageFile!.path),
                            height: imageHeight, // Use dynamic height
                            width: double.infinity,
                            fit: BoxFit.cover,
                          ),
                        )
                      : Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(
                              Icons.add_photo_alternate_outlined, // Changed icon
                              size: 48,
                              color: Colors.grey.shade400,
                            ),
                            const SizedBox(height: 8),
                            Text(
                              "Tap to select an image (${widget.modalityName})", // Updated text
                              style: TextStyle(color: Colors.grey.shade500),
                            ),
                          ],
                        ),
                ),
              ),
            ),
            const SizedBox(height: 32),
            if (_isAnalyzing)
              const Center(child: CircularProgressIndicator())
            else
              ElevatedButton.icon(
                onPressed: () {
                  // Check if this is a multi-model analysis
                  if (widget.modelName.contains("All")) {
                    _runMultiModelAnalysis();
                  } else {
                    _runSingleModelAnalysis();
                  }
                },
                icon: const Icon(Icons.biotech),
                label: const Text("Analyze Image"),
                style: ElevatedButton.styleFrom(
                  backgroundColor: theme.primaryColor,
                  foregroundColor: Colors.white,
                ),
              ),
          ],
        ),
      ),
    );
  }
}
