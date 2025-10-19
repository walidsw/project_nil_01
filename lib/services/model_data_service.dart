import 'package:flutter/material.dart';

// --- Data Structures ---

class MLModel {
  final String id;
  final String name;
  final String description;

  MLModel({required this.id, required this.name, required this.description});
}

class Modality {
  final String name;
  final IconData icon;
  final List<MLModel> models;

  Modality({required this.name, required this.icon, required this.models});
}

class Disease {
  final String name;
  final IconData icon;
  final Color color;
  final List<Modality> modalities;

  Disease({required this.name, required this.icon, required this.color, required this.modalities});
}

// --- Data Service ---

class ModelDataService {
  static final List<Disease> _diseases = [
    // --- Neurological Disorders ---
    Disease(
      name: "Neurological Disorders",
      icon: Icons.psychology,
      color: Colors.blue.shade700,
      modalities: [
        Modality(
          name: "Brain MRI",
          icon: Icons.scanner,
          models: [
            MLModel(id: "alz-mri-resnet", name: "Alzheimer's ResNet", description: "Detects early signs of Alzheimer's using ResNet architecture."),
            MLModel(id: "alz-mri-vgg", name: "Alzheimer's VGG16", description: "Analyzes MRI scans for Alzheimer's patterns with VGG16."),
            MLModel(id: "tumor-mri-seg", name: "Brain Tumor Segmentation", description: "Segments tumor regions in brain MRI scans."),
          ],
        ),
        Modality(
          name: "PET Scan",
          icon: Icons.flare,
          models: [
            MLModel(id: "alz-pet-unet", name: "PET Scan U-Net", description: "Segments amyloid plaques in PET scans."),
            MLModel(id: "alz-pet-gan", name: "PET Scan GAN", description: "Generates predictive models for disease progression."),
          ],
        ),
        Modality(
          name: "CT Scan",
          icon: Icons.fullscreen,
          models: [
            MLModel(id: "stroke-ct-cnn", name: "Stroke Detection CNN", description: "Identifies ischemic strokes from head CT scans."),
          ],
        ),
      ],
    ),

    // --- Cancer ---
    Disease(
      name: "Oncology (Cancer)",
      icon: Icons.healing,
      color: Colors.purple.shade700,
      modalities: [
        Modality(
          name: "Dermatoscopic Image",
          icon: Icons.texture,
          models: [
            MLModel(id: "skin-cancer-effnet", name: "Skin Cancer EfficientNet", description: "Classifies skin lesions as benign or malignant."),
            MLModel(id: "skin-cancer-mobilenet", name: "Skin Cancer MobileNet", description: "A lightweight model for rapid skin lesion analysis."),
          ],
        ),
        Modality(
          name: "Mammogram",
          icon: Icons.bubble_chart,
          models: [
            MLModel(id: "breast-cancer-mammo", name: "Breast Cancer Detection", description: "Identifies suspicious masses in mammograms."),
          ],
        ),
      ],
    ),

    // --- Thoracic Diseases ---
    Disease(
      name: "Thoracic Diseases",
      icon: Icons.science_outlined,
      color: Colors.teal.shade700,
      modalities: [
        Modality(
          name: "Chest X-Ray",
          icon: Icons.camera_alt,
          models: [
            MLModel(id: "pneumonia-xray-cnn", name: "Pneumonia Detection CNN", description: "Identifies signs of pneumonia from chest X-ray images."),
            MLModel(id: "pneumonia-xray-densenet", name: "Pneumonia DenseNet", description: "A deep learning model for pneumonia classification."),
          ],
        ),
      ],
    ),
  ];

  static List<Disease> getDiseases() {
    return _diseases;
  }
}