import 'package:flutter/material.dart';
import 'modality_selection_screen.dart';

class ModelListScreen extends StatelessWidget {
  const ModelListScreen({super.key});

  final List<Map<String, dynamic>> models = const [
    {
      'name': 'Breast Cancer Classification',
      'icon': '🩸',
      'detail': 'Analyzes mammograms for early stage tumor detection.',
      'modalities': ['Mammogram', 'Ultrasound', 'MRI Scan'],
      'color': Color(0xFF2196F3), // Blue
    },
    {
      'name': 'Glioma Tumor Segmentation',
      'icon': '🧠',
      'detail': 'Segments and classifies brain tumors from MRI scans.',
      'modalities': ['MRI Scan', 'CT Scan'],
      'color': Color(0xFFFF9800), // Orange
    },
    {
      'name': 'Alzheimer\'s Progression Tracker',
      'icon': '🧪',
      'detail': 'Predicts disease stage based on patient data and brain scans.',
      'modalities': ['MRI Scan', 'PET Scan'],
      'color': Color(0xFF2196F3), // Blue
    },
    {
      'name': 'Diabetic Retinopathy Detection',
      'icon': '👁️',
      'detail': 'Identifies signs of damage in retinal images.',
      'modalities': ['Fundus Photography', 'OCT Scan'],
      'color': Color(0xFFFF9800), // Orange
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.blue.shade100, // Add this line
        title: const Text('Available Medical Models'),
        centerTitle: false,
      ),
      body: Padding(
        padding: const EdgeInsets.only(top: 8.0, left: 16.0, right: 16.0),
        child: ListView.builder(
          itemCount: models.length,
          itemBuilder: (context, index) {
            final model = models[index];
            final cardColor = model['color'] as Color;

            return SizedBox(
              height: 150, // Fixed height for all cards
              child: Card(
                color: cardColor.withValues(alpha: 0.05),
                margin: const EdgeInsets.only(bottom: 12),
                child: ListTile(
                  contentPadding: const EdgeInsets.all(16),
                  leading: CircleAvatar(
                    backgroundColor: cardColor.withValues(alpha: 0.2),
                    child: Text(
                      model['icon']! as String,
                      style: const TextStyle(fontSize: 24),
                    ),
                  ),
                  title: Text(
                    model['name']! as String,
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                  ),
                  subtitle: Padding(
                    padding: const EdgeInsets.only(top: 4.0),
                    child: Text(
                      model['detail']! as String,
                      style: TextStyle(color: Colors.grey.shade600),
                      maxLines: 2, // Limit to 2 lines
                      overflow: TextOverflow.ellipsis, // Add ellipsis if text is too long
                    ),
                  ),
                  trailing: Icon(Icons.chevron_right, color: cardColor),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => ModalitySelectionScreen(
                          modelName: model['name']! as String,
                          modelDescription: model['detail']! as String,
                          availableModalities: model['modalities']! as List<String>,
                        ),
                      ),
                    );
                  },
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}
