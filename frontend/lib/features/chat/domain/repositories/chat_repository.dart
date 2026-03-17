import 'package:dartz/dartz.dart';

import '../../../../core/error/failures.dart';
import '../entities/chat_room.dart';
import '../entities/message.dart';

/// Chat Repository 인터페이스
/// Data Layer에서 구현
abstract class ChatRepository {
  /// 내가 속한 채팅방 목록 조회
  Future<Either<Failure, List<ChatRoom>>> getRooms();

  /// 채팅방 생성
  Future<Either<Failure, String>> createRoom({
    required List<String> members,
  });

  /// 채팅방 나가기
  Future<Either<Failure, void>> exitRoom({
    required String roomId,
    required String userId,
  });

  /// 채팅방에 멤버 초대
  Future<Either<Failure, void>> inviteMember({
    required String roomId,
    required String targetUserId,
    required String senderId,
  });

  /// 채팅방 메시지 히스토리 조회
  Future<Either<Failure, List<Message>>> getMessages({
    required String roomId,
    String? lastMessageId,
  });

  /// WebSocket으로 메시지 전송
  Future<Either<Failure, void>> sendMessage({
    required String roomId,
    required String messageType,
    String? content,
    Map<String, dynamic>? media,
  });

  /// WebSocket 연결 (token: JWT access token)
  Future<Either<Failure, void>> connectWebSocket(String token);

  /// WebSocket 연결 해제
  Future<Either<Failure, void>> disconnectWebSocket();

  /// 실시간 메시지 수신 스트림
  Stream<Message> get messageStream;

  /// WebSocket 연결 상태 스트림
  Stream<bool> get connectionStream;
}
