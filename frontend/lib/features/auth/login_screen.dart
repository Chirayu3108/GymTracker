import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  bool _isLoading = false;

  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Log In")),
      body: Padding(
        padding: const EdgeInsets.all(50),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              // ----------- Email --------------
              TextFormField(
                controller: _emailController,
                decoration: const InputDecoration(labelText: "Email"),
                validator: (value) {
                  if (value == null || !value.contains("@")) {
                    return "Enter a valid Email";
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              // ---------------------------------
              // ------------ Password -----------
              TextFormField(
                controller: _passwordController,
                obscuringCharacter: "*",
                obscureText: true,
                decoration: const InputDecoration(labelText: "Password"),
                validator: (value) {
                  if (value == null || value.length < 8) {
                    return "Password should be more than 8 letters";
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              // ---------------------------------
              // --------- Log In Button ---------
              ElevatedButton(
                onPressed: _isLoading ? null : _login,
                child: const Text("Log In"),
              ),
              // --------------------------------
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _login() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      _isLoading = true;
    });

    final dio = Dio();

    try {
      final response = await dio.post(
        "http://127.0.0.1:8000/api/v1/auth/login",
        data: {
          "email": _emailController.text,
          "password": _passwordController.text,
        },
      );

      final responseData = response.data as Map<String, dynamic>;
      final accessToken = responseData['access_token'] as String?;
      final refreshToken = responseData['refresh_token'] as String?;

      if (accessToken == null || refreshToken == null) {
        throw Exception("Tokens missing in login response");
      }

      const storage = FlutterSecureStorage();
      await storage.write(key: 'access_token', value: accessToken);
      await storage.write(key: 'refresh_token', value: refreshToken);

      print(await storage.read(key: 'access_token'));
      if (mounted) {
        context.go("/home");
      }
    } on DioException catch (e) {
      if (!mounted) return;
      final message =
          e.response?.data['detail'] ?? "Something went wrong. Try again later";
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text(message)));
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }
}
