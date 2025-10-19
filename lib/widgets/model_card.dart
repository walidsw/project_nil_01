import 'package:flutter/material.dart';

class ModelCard extends StatelessWidget {
  final String title;
  final String description;
  final IconData icon;
  final VoidCallback onTap;

  const ModelCard({
    super.key,
    required this.title,
    required this.description,
    required this.icon,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              // Header with Icon and Title
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(icon, size: 36, color: theme.primaryColor),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      title,
                      style: theme.textTheme.titleMedium,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                ],
              ),
              // Description
              Padding(
                padding: const EdgeInsets.only(top: 8.0),
                child: Text(
                  description,
                  style: theme.textTheme.bodyMedium?.copyWith(color: Colors.grey.shade600),
                  maxLines: 3,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              // "Select" indicator at the bottom
              Align(
                alignment: Alignment.bottomRight,
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      'Select',
                      style: theme.textTheme.labelLarge?.copyWith(color: theme.primaryColor),
                    ),
                    const SizedBox(width: 4),
                    Icon(Icons.arrow_forward, size: 16, color: theme.primaryColor),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}