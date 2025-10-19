import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const MedicalMLPlatform());
}

class MedicalMLPlatform extends StatelessWidget {
  const MedicalMLPlatform({super.key});

  // Define a new, more vibrant color palette
  static const Color _primaryColor = Color(0xFF0D47A1); // A deep, professional blue
  static const Color _secondaryColor = Color(0xFF00897B); // A vibrant teal
  static const Color _backgroundColor = Color(0xFFF5F7FA); // A light, clean background

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Medical ML Platform',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primaryColor: _primaryColor,
        scaffoldBackgroundColor: _backgroundColor, // Set the background color for all scaffolds
        colorScheme: ColorScheme.fromSeed(
          seedColor: _primaryColor,
          secondary: _secondaryColor,
          brightness: Brightness.light,
        ),
        useMaterial3: true,
        appBarTheme: const AppBarTheme(
          backgroundColor: _backgroundColor, // Clean background for AppBar
          surfaceTintColor: Colors.transparent, // Removes tint on scroll
          elevation: 0,
          foregroundColor: Colors.black87, // Dark text and icons
          centerTitle: true,
        ),
        cardTheme: CardThemeData(
          elevation: 1,
          color: Colors.white, // White cards to pop against the background
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: _primaryColor,
            foregroundColor: Colors.white,
            padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 24),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
      ),
      home: const HomeScreen(),
    );
  }
}
