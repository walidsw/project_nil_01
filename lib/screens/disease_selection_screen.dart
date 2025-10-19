import 'package:flutter/material.dart';
import '../services/model_data_service.dart';
import 'modality_selection_screen.dart';

class DiseaseSelectionScreen extends StatelessWidget {
  const DiseaseSelectionScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final diseases = ModelDataService.getDiseases();

    return Scaffold(
      appBar: AppBar(
        title: const Text("Step 1: Select Disease Category"),
      ),
      body: ListView.builder(
        padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 24.0),
        itemCount: diseases.length,
        itemBuilder: (context, index) {
          final disease = diseases[index];
          return Card(
            elevation: 3,
            margin: const EdgeInsets.only(bottom: 16),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
            clipBehavior: Clip.antiAlias, // Ensures the border is clipped correctly
            child: InkWell(
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => ModalitySelectionScreen(disease: disease),
                  ),
                );
              },
              child: Container(
                // Add a decorative left border with the disease color
                decoration: BoxDecoration(
                  border: Border(
                    left: BorderSide(color: disease.color, width: 6),
                  ),
                ),
                child: Padding(
                  // Increased padding to make the card taller
                  padding: const EdgeInsets.symmetric(vertical: 24.0, horizontal: 16.0),
                  child: Row(
                    children: [
                      Icon(disease.icon, size: 40, color: disease.color),
                      const SizedBox(width: 20),
                      Expanded(
                        child: Text(
                          disease.name,
                          // Increased font size
                          style: const TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 18,
                          ),
                        ),
                      ),
                      const Icon(Icons.arrow_forward_ios, color: Colors.grey),
                    ],
                  ),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}