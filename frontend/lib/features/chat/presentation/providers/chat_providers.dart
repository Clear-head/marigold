import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/providers/core_providers.dart';
import '../../data/datasources/chat_remote_datasource.dart';
import '../../data/datasources/chat_websocket_datasource.dart';
import '../../data/repositories/chat_repository_impl.dart';
import '../../domain/entities/chat_room.dart';
import '../../domain/entities/message.dart';
import '../../domain/repositories/chat_repository.dart';

/// ChatRemoteDataSource Provider
final chatRemoteDataSourceProvider = Provider<ChatRemoteDataSource>((ref) {
  final dioClient = ref.watch(chatDioClientProvider);
  return ChatRemoteDataSourceImpl(dioClient: dioClient);
});

/// ChatWebSocketDataSource Provider
final chatWebSocketDataSourceProvider =
    Provider<ChatWebSocketDataSource>((ref) {
  final webSocketClient = ref.watch(webSocketClientProvider);
  return ChatWebSocketDataSourceImpl(webSocketClient: webSocketClient);
});

/// ChatRepository Provider
final chatRepositoryProvider = Provider<ChatRepository>((ref) {
  final remoteDataSource = ref.watch(chatRemoteDataSourceProvider);
  final webSocketDataSource = ref.watch(chatWebSocketDataSourceProvider);

  return ChatRepositoryImpl(
    remoteDataSource: remoteDataSource,
    webSocketDataSource: webSocketDataSource,
  );
});

/// 채팅방 목록 Provider
final chatRoomsProvider = FutureProvider.autoDispose<List<ChatRoom>>((ref) async {
  final repository = ref.watch(chatRepositoryProvider);
  final result = await repository.getRooms();

  return result.fold(
    (failure) => throw Exception(failure.toString()),
    (rooms) => rooms,
  );
});

/// 특정 채팅방의 메시지 히스토리 Provider
final chatMessagesProvider = FutureProvider.autoDispose
    .family<List<Message>, String>((ref, roomId) async {
  final repository = ref.watch(chatRepositoryProvider);
  final result = await repository.getMessages(roomId: roomId);

  return result.fold(
    (failure) => throw Exception(failure.toString()),
    (messages) => messages,
  );
});

/// 실시간 메시지 스트림 Provider
final realtimeMessagesProvider = StreamProvider.autoDispose<Message>((ref) {
  final repository = ref.watch(chatRepositoryProvider);
  return repository.messageStream;
});

/// WebSocket 연결 상태 Provider
final chatConnectionStatusProvider = StreamProvider.autoDispose<bool>((ref) {
  final repository = ref.watch(chatRepositoryProvider);
  return repository.connectionStream;
});

/// WebSocket 연결 Provider (token: JWT access token)
final chatWebSocketConnectionProvider =
    FutureProvider.autoDispose.family<void, String>((ref, token) async {
  final repository = ref.watch(chatRepositoryProvider);
  final result = await repository.connectWebSocket(token);

  result.fold(
    (failure) => throw Exception(failure.toString()),
    (_) => null,
  );
});
