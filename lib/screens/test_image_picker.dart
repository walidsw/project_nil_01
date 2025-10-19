import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';

class TestImagePicker extends StatefulWidget {
  const TestImagePicker({super.key});

  @override
  State<TestImagePicker> createState() => _TestImagePickerState();
}

class _TestImagePickerState extends State<TestImagePicker> {
  File? _image;
  final ImagePicker _picker = ImagePicker();

  Future<void> _pickImage() async {
    print('=== STARTING IMAGE PICK ===');
    try {
      final XFile? image = await _picker.pickImage(source: ImageSource.gallery);
      print('=== IMAGE PICK RESULT: ${image?.path} ===');

      if (image != null) {
        setState(() {
          _image = File(image.path);
        });
        print('=== IMAGE SET SUCCESSFULLY ===');

        // Show success message
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('✅ Image loaded successfully!'),
            backgroundColor: Colors.green,
          ),
        );
      } else {
        print('=== NO IMAGE SELECTED ===');
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('❌ No image selected'),
            backgroundColor: Colors.orange,
          ),
        );
      }
    } catch (e) {
      print('=== ERROR: $e ===');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('❌ Error: $e'), backgroundColor: Colors.red),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Image Picker Test'),
        backgroundColor: Colors.blue,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Image display
            Container(
              width: 200,
              height: 200,
              decoration: BoxDecoration(
                border: Border.all(color: Colors.grey),
                borderRadius: BorderRadius.circular(8),
              ),
              child: _image != null
                  ? ClipRRect(
                      borderRadius: BorderRadius.circular(8),
                      child: Image.file(_image!, fit: BoxFit.cover),
                    )
                  : const Center(child: Text('No Image')),
            ),
            const SizedBox(height: 20),

            // Pick button
            ElevatedButton.icon(
              onPressed: _pickImage,
              icon: const Icon(Icons.photo_library),
              label: const Text('Pick Image'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.blue,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(
                  horizontal: 20,
                  vertical: 10,
                ),
              ),
            ),

            const SizedBox(height: 20),

            // Status text
            Text(
              _image != null ? '✅ Image loaded!' : 'No image selected',
              style: TextStyle(
                color: _image != null ? Colors.green : Colors.grey,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
