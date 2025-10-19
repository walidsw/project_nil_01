import 'package:flutter/material.dart';
import '../services/model_data_service.dart';
import 'model_list_screen.dart';

class ModalitySelectionScreen extends StatelessWidget {
  final Disease disease;

  const ModalitySelectionScreen({super.key, required this.disease});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Step 2: Select Modality"),
        backgroundColor: disease.color.withOpacity(0.8),
        foregroundColor: Colors.white,
      ),
      body: GridView.builder(
        padding: const EdgeInsets.all(16.0),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          crossAxisSpacing: 16,
          mainAxisSpacing: 16,
          childAspectRatio: 1.0,
        ),
        itemCount: disease.modalities.length,
        itemBuilder: (context, index) {
          final modality = disease.modalities[index];
          return InkWell(
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => ModelListScreen(
                    diseaseName: disease.name,
                    modality: modality,
                  ),
                ),
              );
            },
            child: Card(
              elevation: 4,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(modality.icon, size: 50, color: disease.color),
                  const SizedBox(height: 16),
                  Text(
                    modality.name,
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                    textAlign: TextAlign.center,
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
