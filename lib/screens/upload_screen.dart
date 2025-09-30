import 'package:flutter/material.dart';
import 'result_screen.dart';

class UploadScreen extends StatelessWidget {
  final String modelName;
  UploadScreen({required this.modelName});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Upload Input for $modelName")),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            // TODO: Integrate with file picker / API
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => ResultScreen(modelName: modelName),
              ),
            );
          },
          child: Text("Upload File & Run Model"),
        ),
      ),
    );
  }
}
