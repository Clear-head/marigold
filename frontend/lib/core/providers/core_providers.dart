import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:logger/logger.dart';

import '../constants/api_constants.dart';
import '../network/dio_client.dart';
import '../network/websocket_client.dart';
import '../storage/token_storage.dart';

/// Logger Provider
final loggerProvider = Provider<Logger>((ref) {
  return Logger(
    printer: PrettyPrinter(
      methodCount: 2,
      errorMethodCount: 8,
      lineLength: 120,
      colors: true,
      printEmojis: true,
      dateTimeFormat: DateTimeFormat.onlyTimeAndSinceStart,
    ),
  );
});

/// TokenStorage Provider
final tokenStorageProvider = Provider<TokenStorage>((ref) {
  final logger = ref.watch(loggerProvider);
  return TokenStorage(logger: logger);
});

/// DioClient Provider (Chat Service)
final chatDioClientProvider = Provider<DioClient>((ref) {
  final tokenStorage = ref.watch(tokenStorageProvider);
  final logger = ref.watch(loggerProvider);

  return DioClient(
    tokenStorage: tokenStorage,
    logger: logger,
  );
});

/// DioClient Provider (Auth Service)
final authDioClientProvider = Provider<DioClient>((ref) {
  final tokenStorage = ref.watch(tokenStorageProvider);
  final logger = ref.watch(loggerProvider);

  return DioClient(
    tokenStorage: tokenStorage,
    logger: logger,
    baseUrl: ApiConstants.authBaseUrl,
  );
});

/// WebSocketClient Provider
final webSocketClientProvider = Provider<WebSocketClient>((ref) {
  final logger = ref.watch(loggerProvider);
  final client = WebSocketClient(logger: logger);

  // Provider가 dispose될 때 WebSocket 연결 종료
  ref.onDispose(() {
    client.dispose();
  });

  return client;
});

/// WebSocket 연결 상태 Provider
final webSocketStatusProvider = StreamProvider.autoDispose((ref) {
  final client = ref.watch(webSocketClientProvider);
  return client.statusStream;
});

/// WebSocket 메시지 스트림 Provider
final webSocketMessageProvider = StreamProvider.autoDispose((ref) {
  final client = ref.watch(webSocketClientProvider);
  return client.messageStream;
});

/// 인증 상태 Provider
final isAuthenticatedProvider = FutureProvider.autoDispose<bool>((ref) async {
  final tokenStorage = ref.watch(tokenStorageProvider);
  return await tokenStorage.isAuthenticated();
});

/// 현재 User ID Provider
final currentUserIdProvider = FutureProvider.autoDispose<String?>((ref) async {
  final tokenStorage = ref.watch(tokenStorageProvider);
  return await tokenStorage.getUserId();
});
