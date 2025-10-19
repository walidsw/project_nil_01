import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

class TestImagePicker extends StatefulWidget {
  const TestImagePicker({super.key});

  @override
  State<TestImagePicker> createState() => _TestImagePickerState();
}

class _TestImagePickerState extends State<TestImagePicker> {
  File? _imageFile;
  final ImagePicker _picker = ImagePicker();

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
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Test Image Picker'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (_imageFile != null)
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Image.file(_imageFile!, height: 300),
              )
            else
              const Text('No image selected.'),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _pickImage,
              child: const Text('Pick Image from Gallery'),
            ),
          ],
        ),
      ),
    );
  }
}
