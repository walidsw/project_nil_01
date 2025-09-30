import 'package:flutter/material.dart';

class ResultScreen extends StatelessWidget {
  final String modelName;
  ResultScreen({required this.modelName});

  @override
  Widget build(BuildContext context) {
    // Dummy results
    final List<String> results = [
      "$modelName → Positive",
      "Other Model 1 → Positive",
      "Other Model 2 → Negative",
    ];
    final String combinedResult = "2 out of 3 predicted Positive";

    return Scaffold(
      appBar: AppBar(title: Text("Results")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("Individual Model Results:",
                style: TextStyle(fontWeight: FontWeight.bold)),
            ...results.map((r) => ListTile(title: Text(r))),
            Divider(),
            Text("Combined Result:",
                style: TextStyle(fontWeight: FontWeight.bold)),
            ListTile(title: Text(combinedResult)),
          ],
        ),
      ),
    );
  }
}
