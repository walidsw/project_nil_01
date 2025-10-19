import 'package:flutter/material.dart';
import '../services/model_data_service.dart';
import '../widgets/model_card.dart';
import 'upload_screen.dart';

class ModelListScreen extends StatelessWidget {
  final String diseaseName;
  final Modality modality;

  const ModelListScreen({
    super.key,
    required this.diseaseName,
    required this.modality,
  });

  @override
  Widget build(BuildContext context) {
    final models = modality.models;

    return Scaffold(
      appBar: AppBar(
        title: const Text("Step 3: Select Model"),
      ),
      body: Column(
        children: [
          // "Use All" Button
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 16, 16, 0),
            child: ElevatedButton.icon(
              icon: const Icon(Icons.select_all),
              label: Text("Analyze with all ${modality.name} models"),
              style: ElevatedButton.styleFrom(
                minimumSize: const Size(double.infinity, 50),
                backgroundColor: Theme.of(context).colorScheme.secondary,
              ),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => UploadScreen(
                      modelName: "All ${modality.name} Models",
                      modelDescription: "Upload an image to run analysis against all available models for this modality.",
                      modalityName: modality.name,
                    ),
                  ),
                );
              },
            ),
          ),
          const Padding(
            padding: EdgeInsets.all(16.0),
            child: Row(
              children: [
                Expanded(child: Divider()),
                Padding(
                  padding: EdgeInsets.symmetric(horizontal: 8.0),
                  child: Text("OR", style: TextStyle(color: Colors.grey)),
                ),
                Expanded(child: Divider()),
              ],
            ),
          ),
          // Grid of individual models
          Expanded(
            child: GridView.builder(
              padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
              gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
                maxCrossAxisExtent: 400.0,
                childAspectRatio: 1.1,
                crossAxisSpacing: 20.0,
                mainAxisSpacing: 20.0,
              ),
              itemCount: models.length,
              itemBuilder: (context, index) {
                final model = models[index];
                return ModelCard(
                  title: model.name,
                  description: model.description,
                  icon: Icons.biotech, // Generic icon for models
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => UploadScreen(
                          modelName: model.name,
                          modelDescription: model.description,
                          modalityName: modality.name,
                        ),
                      ),
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
