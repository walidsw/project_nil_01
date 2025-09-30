import 'package:flutter/material.dart';
import 'upload_screen.dart';

class ModelListScreen extends StatefulWidget {
  final String category;
  const ModelListScreen({required this.category});

  @override
  State<ModelListScreen> createState() => _ModelListScreenState();
}

class _ModelListScreenState extends State<ModelListScreen> {
  final Map<String, List<String>> models = {
    "Alzheimer": ["MRI Model 1", "MRI Model 2", "Data Model 1"],
    "Cancer": ["Model A", "Model B"],
    "Tumor": ["Brain Tumor Model 1", "Skin Tumor Model 2"],
  };

  @override
  Widget build(BuildContext context) {
    final modelList = models[widget.category] ?? [];

    return Scaffold(
      appBar: AppBar(title: Text("${widget.category} Models")),
      body: ListView.builder(
        itemCount: modelList.length,
        itemBuilder: (context, index) {
          return Card(
            child: ListTile(
              title: Text(modelList[index]),
              trailing: Icon(Icons.upload_file),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) =>
                        UploadScreen(modelName: modelList[index]),
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}
