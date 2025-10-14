import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import 'result_screen.dart';

class UploadScreen extends StatefulWidget {
  final String modelName;
  final String modelDescription;
  final String modalityName; // New parameter to show input type (e.g., MRI, X-Ray)

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
  File? _imageFile;
  final ImagePicker _picker = ImagePicker();
  bool _isLoading = false;

  // --- Image Picking Logic ---
  Future<void> _pickImage() async {
    try {
      final pickedFile = await _picker.pickImage(source: ImageSource.gallery);
      if (pickedFile != null) {
        setState(() {
          _imageFile = File(pickedFile.path);
        });
      }
    } catch (e) {
      debugPrint('Image pick error: $e');
      // In a real app, show a snackbar or alert here
    }
  }

  // --- Model Run Placeholder ---
  Future<void> _runModelAndNavigate() async {
    if (_imageFile == null) return;

    setState(() {
      _isLoading = true;
    });

    // --- Placeholder for ML Model Execution (Simulated Delay) ---
    await Future.delayed(const Duration(seconds: 2));

    setState(() {
      _isLoading = false;
    });

    // Check if widget is still mounted before navigation
    if (!mounted) return;

    // Navigate to result screen
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => ResultScreen(
          modelName: widget.modelName,
          imageFile: _imageFile!,
          modelResult: "Malignant (94.5% Confidence)", 
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.modelName),
        backgroundColor: Colors.blue.shade100, 
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // --- Model Information Card ---
            Card(
              color: theme.primaryColor.withValues(alpha: 0.05), // Changed from withOpacity
              elevation: 0,
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "Input Required: ${widget.modalityName}",
                      style: theme.textTheme.titleMedium?.copyWith(color: theme.primaryColor),
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

            // --- Image Preview Area ---
            Container(
              height: 250,
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
                          _imageFile!,
                          height: 250,
                          fit: BoxFit.cover,
                        ),
                      )
                    : Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.image, size: 48, color: Colors.grey.shade400),
                          const SizedBox(height: 8),
                          Text(
                            "Select an image file (${widget.modalityName})",
                            style: TextStyle(color: Colors.grey.shade500),
                          ),
                        ],
                      ),
              ),
            ),
            const SizedBox(height: 32),

            // --- Pick Image Button ---
            ElevatedButton.icon(
              onPressed: _pickImage,
              icon: const Icon(Icons.photo_library),
              label: const Text("Select Image from Gallery"),
              style: ElevatedButton.styleFrom(
                backgroundColor: theme.primaryColor,
                foregroundColor: Colors.white,
              ),
            ),
            const SizedBox(height: 16),

            // --- Upload and Run Button ---
            ElevatedButton(
              onPressed: _imageFile == null || _isLoading ? null : _runModelAndNavigate,
              style: ElevatedButton.styleFrom(
                backgroundColor: _imageFile == null ? Colors.grey : theme.colorScheme.secondary,
                foregroundColor: Colors.white,
              ),
              child: _isLoading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(
                        color: Colors.white,
                        strokeWidth: 3,
                      ),
                    )
                  : const Text("Analyze & Get Prediction"),
            ),
          ],
        ),
      ),
    );
  }
}
