import "package:flutter/material.dart";
import 'package:dio/dio.dart';
import 'package:go_router/go_router.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  bool _isLoading = false;

  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _displayNameController = TextEditingController();

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    _displayNameController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Sign Up")),
      body: Padding(
        padding: const EdgeInsets.all(50),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              // -------- Display Name -------
              TextFormField(
                controller: _displayNameController,
                decoration: const InputDecoration(labelText: "Your Name"),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return "Enter Your Name";
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              // -----------------------------

              // ----------- Email -------------
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
              // ------------------------------

              // ------- Password ---------
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
              // -----------------------------

              // ------------- Submit Button -------------------
              ElevatedButton(
                onPressed: _isLoading ? null : _submit,
                child: const Text("Sign Up"),
              ),
              // --------------------------------------------

              // ------------- Text Button ----------------------
              TextButton(
                onPressed: () => context.go("/login"),
                child: const Text("Already have an account? Log in"),
              ),

              // ------------------------------------------------
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      _isLoading = true;
    });

    final dio = Dio();

    try {
      await dio.post(
        "http://127.0.0.1:8000/api/v1/auth/register",
        data: {
          "email": _emailController.text,
          "password": _passwordController.text,
          "display_name": _displayNameController.text,
        },
      );
      // ---------- Successful Sign Up ---------------
      if (mounted) {
        context.go("/login");
      }
      // ------------------ Else -------------------
    } on DioException catch (e) {
      if (!mounted) return;
      final message =
          e.response?.data['detail'] ?? "Something went wrong. Try Again.";
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text(message)));
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
        // -------------------------------------------
      }
    }
  }
}
