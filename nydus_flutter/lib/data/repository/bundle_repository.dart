import 'dart:convert';
import 'package:flutter/services.dart';
import '../models/bundle_data.dart';

class BundleRepository {
  Future<BundleData> load() async {
    final jsonString = await rootBundle.loadString('assets/graphs.json');
    final raw = jsonDecode(jsonString) as Map<String, dynamic>;
    return BundleData.fromJson(raw);
  }
}
