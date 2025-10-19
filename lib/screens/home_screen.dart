import 'package:flutter/material.dart';
import 'model_list_screen.dart';
import 'test_image_picker.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.blue.shade100, // Add this line
        foregroundColor: Colors.white, // Add this line for white text/icons
        title: const Text('Medical ML Platform'),
        actions: [
          IconButton(
            icon: const Icon(Icons.photo_camera),
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => const TestImagePicker()),
            ),
            tooltip: 'Test Image Picker',
          ),
          IconButton(
            icon: const Icon(Icons.info_outline),
            onPressed: () => _showAboutDialog(context),
            tooltip: 'About',
          ),
        ],
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Hero Section
                _buildHeroSection(context, theme),

                const SizedBox(height: 32),

                // Features Grid
                _buildFeaturesGrid(context, theme),

                const SizedBox(height: 32),

                // Main Action Button
                _buildMainActionButton(context, theme),

                const SizedBox(height: 24),

                // Statistics Section
                _buildStatisticsSection(context, theme),

                const SizedBox(height: 16),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildHeroSection(BuildContext context, ThemeData theme) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            theme.primaryColor.withValues(alpha: 0.1),
            theme.colorScheme.secondary.withValues(alpha: 0.1),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(Icons.local_hospital, size: 48, color: theme.primaryColor),
          const SizedBox(height: 16),
          Text(
            'AI-Powered Medical Diagnostics',
            style: theme.textTheme.titleLarge?.copyWith(
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            'Upload medical images and get instant AI-powered analysis using state-of-the-art machine learning models.',
            style: theme.textTheme.bodyMedium?.copyWith(
              color: Colors.grey[700],
              height: 1.5,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildFeaturesGrid(BuildContext context, ThemeData theme) {
    final features = [
      {
        'icon': Icons.speed,
        'title': 'Fast Analysis',
        'description': 'Get results in seconds',
        'color': const Color(0xFF4CAF50), // Green
      },
      {
        'icon': Icons.security,
        'title': 'Secure & Private',
        'description': 'Your data is protected',
        'color': const Color(0xFF2196F3), // Blue
      },
      {
        'icon': Icons.verified,
        'title': 'High Accuracy',
        'description': 'AI-powered precision',
        'color': const Color(0xFFFF9800), // Orange
      },
      {
        'icon': Icons.analytics,
        'title': 'Detailed Reports',
        'description': 'Comprehensive insights',
        'color': const Color(0xFF9C27B0), // Purple
      },
    ];

    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 12,
        mainAxisSpacing: 12,
        childAspectRatio: 1.1,
      ),
      itemCount: features.length,
      itemBuilder: (context, index) {
        final feature = features[index];
        final cardColor = feature['color'] as Color;

        return Card(
          color: cardColor.withValues(alpha: 0.1),
          elevation: 2,
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(feature['icon'] as IconData, size: 36, color: cardColor),
                const SizedBox(height: 12),
                Text(
                  feature['title'] as String,
                  style: theme.textTheme.titleSmall?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: cardColor,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 4),
                Text(
                  feature['description'] as String,
                  style: theme.textTheme.bodySmall?.copyWith(
                    color: Colors.grey[700],
                  ),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  Widget _buildMainActionButton(BuildContext context, ThemeData theme) {
    return ElevatedButton.icon(
      onPressed: () {
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => const ModelListScreen()),
        );
      },
      icon: const Icon(Icons.rocket_launch, size: 24),
      label: const Text('Start Analysis', style: TextStyle(fontSize: 18)),
      style: ElevatedButton.styleFrom(
        padding: const EdgeInsets.symmetric(vertical: 16),
        elevation: 4,
      ),
    );
  }

  Widget _buildStatisticsSection(BuildContext context, ThemeData theme) {
    final stats = [
      {'label': 'Available Models', 'value': '4'},
      {'label': 'Success Rate', 'value': '94%'},
      {'label': 'Processing Time', 'value': '<3s'},
    ];

    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceAround,
      children: stats.map((stat) {
        return Column(
          children: [
            Text(
              stat['value']!,
              style: theme.textTheme.titleLarge?.copyWith(
                fontWeight: FontWeight.bold,
                color: theme.primaryColor,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              stat['label']!,
              style: theme.textTheme.bodySmall?.copyWith(
                color: Colors.grey[600],
              ),
              textAlign: TextAlign.center,
            ),
          ],
        );
      }).toList(),
    );
  }

  void _showAboutDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('About Medical ML Platform'),
        content: const SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                'This platform provides AI-powered medical image analysis using advanced machine learning models.',
                style: TextStyle(height: 1.5),
              ),
              SizedBox(height: 16),
              Text('Features:', style: TextStyle(fontWeight: FontWeight.bold)),
              SizedBox(height: 8),
              Text('• Multiple specialized ML models'),
              Text('• Fast and accurate predictions'),
              Text('• Secure data handling'),
              Text('• Detailed analysis reports'),
              SizedBox(height: 16),
              Text(
                'Version 1.0.0',
                style: TextStyle(fontSize: 12, color: Colors.grey),
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Close'),
          ),
        ],
      ),
    );
  }
}
