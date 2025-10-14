import 'package:flutter/material.dart';
import 'upload_screen.dart';  // Same folder

class ModalitySelectionScreen extends StatelessWidget {
  final String modelName;
  final String modelDescription;
  final List<String> availableModalities;

  const ModalitySelectionScreen({
    super.key,
    required this.modelName,
    required this.modelDescription,
    required this.availableModalities,
  });

  final Map<String, Map<String, dynamic>> modalityDetails = const {
    'MRI Scan': {
      'icon': Icons.scanner,
      'description': 'Magnetic Resonance Imaging for detailed internal body scans',
      'color': Color(0xFF6C5CE7),
    },
    'X-Ray': {
      'icon': Icons.camera_alt,
      'description': 'Radiographic imaging for bone and tissue analysis',
      'color': Color(0xFF00B894),
    },
    'CT Scan': {
      'icon': Icons.hub,
      'description': 'Computed Tomography for cross-sectional imaging',
      'color': Color(0xFFE17055),
    },
    'Ultrasound': {
      'icon': Icons.graphic_eq,
      'description': 'Sound wave imaging for soft tissue examination',
      'color': Color(0xFF0984E3),
    },
    'Mammogram': {
      'icon': Icons.favorite,
      'description': 'Specialized breast imaging for cancer detection',
      'color': Color(0xFFD63031),
    },
    'Fundus Photography': {
      'icon': Icons.remove_red_eye,
      'description': 'Retinal imaging for eye disease detection',
      'color': Color(0xFFFDCB6E),
    },
    'PET Scan': {
      'icon': Icons.local_hospital,
      'description': 'Positron Emission Tomography for metabolic imaging',
      'color': Color(0xFFA29BFE),
    },
    'OCT Scan': {
      'icon': Icons.visibility,
      'description': 'Optical Coherence Tomography for retinal layers',
      'color': Color(0xFFFF7675),
    },
  };

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.blue.shade100, // Add this line
        title: const Text('Select Imaging Modality'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Model Info Header
            Card(
              color: Theme.of(context).primaryColor.withValues(alpha: 0.05), // Changed
              elevation: 0,
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      modelName,
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      modelDescription,
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: Colors.grey[700],
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            
            // Header Section
            Text(
              'Choose Your Imaging Type',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 8),
            Text(
              'Select the type of medical imaging for this analysis',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: Colors.grey[600],
              ),
            ),
            const SizedBox(height: 24),
            
            // Modality Grid
            Expanded(
              child: GridView.builder(
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  crossAxisSpacing: 12,
                  mainAxisSpacing: 12,
                  childAspectRatio: 0.85,
                ),
                itemCount: availableModalities.length,
                itemBuilder: (context, index) {
                  final modalityName = availableModalities[index];
                  final details = modalityDetails[modalityName];
                  if (details == null) return const SizedBox.shrink();
                  
                  return _buildModalityCard(
                    context,
                    modalityName,
                    details,
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildModalityCard(
    BuildContext context,
    String modalityName,
    Map<String, dynamic> details,
  ) {
    final cardColor = details['color'] as Color;
    
    return Card(
      color: cardColor.withValues(alpha: 0.08), // Add this line
      elevation: 2,
      child: InkWell(
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => UploadScreen(
                modelName: modelName,
                modelDescription: modelDescription,
                modalityName: modalityName,
              ),
            ),
          );
        },
        borderRadius: BorderRadius.circular(12),
        child: Container(
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: cardColor.withValues(alpha: 0.2), // Changed to use cardColor
                  shape: BoxShape.circle,
                ),
                child: Icon(
                  details['icon'] as IconData,
                  size: 40,
                  color: cardColor, // Changed to use cardColor
                ),
              ),
              const SizedBox(height: 12),
              Text(
                modalityName,
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 8),
              Flexible(
                child: Text(
                  details['description'] as String,
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: Colors.grey[600],
                  ),
                  textAlign: TextAlign.center,
                  maxLines: 3,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
