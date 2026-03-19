import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:firebase_core/firebase_core.dart'; // 추가
import 'package:firebase_messaging/firebase_messaging.dart'; // 추가
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'firebase_options.dart'; // 자동 생성된 파일

import 'core/providers/core_providers.dart';
import 'features/auth/presentation/screens/login_screen.dart';
import 'features/shell/presentation/screens/main_shell_screen.dart';

// 알림 권한 요청 (토큰 등록은 로그인 후 LoginNotifier에서 처리)
Future<void> setupFCM() async {
  await FirebaseMessaging.instance.requestPermission(
    alert: true,
    badge: true,
    sound: true,
  );
}

void main() async { // async 추가
  // Flutter 엔진 초기화 보장
  WidgetsFlutterBinding.ensureInitialized();

  // .env 로드
  await dotenv.load(fileName: '.env');

  // Firebase 초기화
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  // FCM 설정 실행
  try {
    await setupFCM();
  } catch (e) {
    print('FCM setup failed (ignored): $e');
  }


  runApp(
    const ProviderScope(
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Marigold',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      routes: {
        '/login': (context) => const LoginScreen(),
      },
      home: const _AuthGate(),
    );
  }
}

class _AuthGate extends ConsumerWidget {
  const _AuthGate();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authAsync = ref.watch(isAuthenticatedProvider);

    return authAsync.when(
      data: (isAuthenticated) =>
          isAuthenticated ? const MainShellScreen() : const LoginScreen(),
      loading: () => const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      ),
      error: (_, __) => const LoginScreen(),
    );
  }
}

