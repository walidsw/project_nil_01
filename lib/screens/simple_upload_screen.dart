import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import 'result_screen.dart';

class SimpleUploadScreen extends StatefulWidget {
  final String modelName;
  final String modelDescription;
  final String modalityName;

  const SimpleUploadScreen({
    super.key,
    required this.modelName,
    required this.modelDescription,
    required this.modalityName,
  });

  @override
  State<SimpleUploadScreen> createState() => _SimpleUploadScreenState();
}

class _SimpleUploadScreenState extends State<SimpleUploadScreen> {
  File? _imageFile;
  final ImagePicker _picker = ImagePicker();
  bool _isLoading = false;

  // Simple image picking
  Future<void> _pickImage() async {
    try {
      print('Starting image pick...');
      final pickedFile = await _picker.pickImage(source: ImageSource.gallery);
      print('Image pick result: ${pickedFile?.path}');
      
      if (pickedFile != null) {
        setState(() {
          _imageFile = File(pickedFile.path);
        });
        print('Image file set: ${_imageFile?.path}');
      } else {
        print('No image selected');
      }
    } catch (e) {
      print('Image pick error: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error: $e'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  // Simple model run
  Future<void> _runModel() async {
    if (_imageFile == null) return;

    setState(() {
      _isLoading = true;
    });

    await Future.delayed(const Duration(seconds: 2));

    setState(() {
      _isLoading = false;
    });

    if (!mounted) return;

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => ResultScreen(
          modelName: widget.modelName,
          imageFile: _imageFile!,
          modelResult: "Test Result (95% Confidence)",
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.modelName),
        backgroundColor: Colors.blue.shade100,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Model info
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "Input: ${widget.modalityName}",
                      style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 8),
                    Text(widget.modelDescription),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Image preview
            Container(
              height: 200,
              width: double.infinity,
              decoration: BoxDecoration(
                color: Colors.grey.shade100,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.grey.shade300),
              ),
              child: _imageFile != null
                  ? ClipRRect(
                      borderRadius: BorderRadius.circular(10),
                      child: Image.file(
                        _imageFile!,
                        fit: BoxFit.cover,
                      ),
                    )
                  : const Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.image, size: 48, color: Colors.grey),
                          SizedBox(height: 8),
                          Text("No image selected", style: TextStyle(color: Colors.grey)),
                        ],
                      ),
                    ),
            ),
            const SizedBox(height: 24),

            // Buttons
            ElevatedButton.icon(
              onPressed: _pickImage,
              icon: const Icon(Icons.photo_library),
              label: const Text("Select Image"),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.blue,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 12),
              ),
            ),
            const SizedBox(height: 16),

            ElevatedButton(
              onPressed: _imageFile == null || _isLoading ? null : _runModel,
              style: ElevatedButton.styleFrom(
                backgroundColor: _imageFile == null ? Colors.grey : Colors.green,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 12),
              ),
              child: _isLoading
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Text("Analyze Image"),
            ),
          ],
        ),
      ),
    );
  }
}
