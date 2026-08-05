import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
import 'package:go_router/go_router.dart';

import 'features/auth/register_screen.dart';
import 'features/auth/login_screen.dart';

void main() {
  runApp(const MyApp());
}

final _router = GoRouter(
  initialLocation: "/register",
  routes: [
    GoRoute(
      path: "/register",
      builder: (context, state) => const RegisterScreen(),
    ),
    GoRoute(path: "/login", builder: (context, state) => const LoginScreen()),
  ],
);

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(title: 'GymTracker', routerConfig: _router);
  }
}

class HealthCheckScreen extends StatelessWidget {
  const HealthCheckScreen({super.key});

  Future<String> fetchHealth() async {
    final dio = Dio();
    final response = await dio.get('http://127.0.0.1:8000/health');
    return response.data['status'];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('GymTracker')),
      body: Center(
        child: FutureBuilder<String>(
          future: fetchHealth(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const CircularProgressIndicator();
            }
            if (snapshot.hasError) {
              return Text('Error: ${snapshot.error}');
            }
            return Text('Backend Status: ${snapshot.data}');
          },
        ),
      ),
    );
  }
}
