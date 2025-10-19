import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'disease_selection_screen.dart';
import 'test_image_picker.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Medical ML Platform'),
        backgroundColor: Theme.of(context).scaffoldBackgroundColor,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.photo_camera),
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => const TestImagePicker()),
            ),
            tooltip: 'Test Image Picker',
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            _buildHeader(context),
            const SizedBox(height: 24),
            _buildMainActionButton(context),
            const SizedBox(height: 32),
            _buildSectionTitle("Key Features"),
            _buildFeaturesGrid(context),
            const SizedBox(height: 32),
            _buildFooter(context),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader(BuildContext context) {
    final theme = Theme.of(context);
    return Container(
      color: Colors.blue.shade800,
      padding: const EdgeInsets.symmetric(vertical: 40.0, horizontal: 24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'AI-Powered Medical Diagnostics',
            style: theme.textTheme.headlineSmall?.copyWith(
              color: Colors.white,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            'Upload medical images for instant AI-powered analysis using state-of-the-art machine learning models.',
            style: theme.textTheme.bodyLarge?.copyWith(
              color: Colors.white.withOpacity(0.9),
              height: 1.5,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMainActionButton(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24.0),
      child: ElevatedButton.icon(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => const DiseaseSelectionScreen()),
          );
        },
        icon: const Icon(Icons.rocket_launch, size: 24),
        label: const Text('Start Analysis', style: TextStyle(fontSize: 18)),
        style: ElevatedButton.styleFrom(
          padding: const EdgeInsets.symmetric(vertical: 16),
          backgroundColor: Colors.green.shade600,
          foregroundColor: Colors.white,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        ),
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24.0),
      child: Text(
        title,
        style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
      ),
    );
  }

  Widget _buildFeaturesGrid(BuildContext context) {
    final features = [
      {
        'icon': Icons.speed,
        'title': 'Fast Analysis',
        'description': 'Get results in seconds',
        'color': Colors.blue.shade700,
      },
      {
        'icon': Icons.security,
        'title': 'Secure & Private',
        'description': 'Your data is protected',
        'color': Colors.orange.shade800,
      },
      {
        'icon': Icons.verified_user,
        'title': 'High Accuracy',
        'description': 'AI-powered precision',
        'color': Colors.purple.shade700,
      },
      {
        'icon': Icons.analytics,
        'title': 'Detailed Reports',
        'description': 'Comprehensive insights',
        'color': Colors.teal.shade700,
      },
    ];

    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      padding: const EdgeInsets.all(24.0),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 16,
        mainAxisSpacing: 16,
        childAspectRatio: 1.0,
      ),
      itemCount: features.length,
      itemBuilder: (context, index) {
        final feature = features[index];
        return Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: feature['color'] as Color,
            borderRadius: BorderRadius.circular(16),
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Icon(feature['icon'] as IconData, size: 40, color: Colors.white),
              const SizedBox(height: 12),
              Text(
                feature['title'] as String,
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                  fontSize: 16,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 4),
              Text(
                feature['description'] as String,
                style: TextStyle(color: Colors.white.withOpacity(0.9)),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildFooter(BuildContext context) {
    return Container(
      color: const Color(0xFF263238), // Dark Blue Grey
      padding: const EdgeInsets.symmetric(vertical: 32.0, horizontal: 24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.local_hospital, color: Colors.white, size: 28),
              SizedBox(width: 12),
              Text(
                "Medical ML Platform",
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Text(
            "Leveraging AI to deliver fast, accurate, and secure analysis of medical images, empowering healthcare professionals with advanced diagnostic tools.",
            style: TextStyle(color: Colors.white.withOpacity(0.7), height: 1.5),
          ),
          const Divider(height: 40, color: Colors.white24),
          const Text(
            "Contact Us",
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
          const SizedBox(height: 16),
          _buildContactRow(
            context,
            icon: Icons.phone,
            text: "01946718561",
            onTap: () => launchUrl(Uri.parse("tel:01946718561")),
          ),
          const SizedBox(height: 12),
          _buildContactRow(
            context,
            icon: Icons.public,
            text: "www.medical-ai-platform.com",
            onTap: () => launchUrl(Uri.parse("https://www.google.com")), // Dummy URL
          ),
          const Divider(height: 40, color: Colors.white24),
          Center(
            child: Text(
              "© 2025 Medical ML Platform. All Rights Reserved.",
              style: TextStyle(color: Colors.white.withOpacity(0.5), fontSize: 12),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildContactRow(BuildContext context, {required IconData icon, required String text, required VoidCallback onTap}) {
    return InkWell(
      onTap: onTap,
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 4.0),
        child: Row(
          children: [
            Icon(icon, color: Colors.white70, size: 20),
            const SizedBox(width: 16),
            Text(
              text,
              style: TextStyle(
                color: Colors.blue[300],
                decoration: TextDecoration.underline,
                decorationColor: Colors.blue[300],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
