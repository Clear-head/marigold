import 'package:dartz/dartz.dart';

import '../../../../core/error/exceptions.dart';
import '../../../../core/error/failures.dart';
import '../../domain/entities/chat_room.dart';
import '../../domain/entities/message.dart';
import '../../domain/repositories/chat_repository.dart';
import '../datasources/chat_remote_datasource.dart';
import '../datasources/chat_websocket_datasource.dart';

/// ChatRepository 구현체
class ChatRepositoryImpl implements ChatRepository {
  final ChatRemoteDataSource _remoteDataSource;
  final ChatWebSocketDataSource _webSocketDataSource;

  ChatRepositoryImpl({
    required ChatRemoteDataSource remoteDataSource,
    required ChatWebSocketDataSource webSocketDataSource,
  })  : _remoteDataSource = remoteDataSource,
        _webSocketDataSource = webSocketDataSource;

  @override
  Future<Either<Failure, List<ChatRoom>>> getRooms() async {
    try {
      final rooms = await _remoteDataSource.getRooms();
      return Right(rooms.map((model) => model.toEntity()).toList());
    } on ServerException catch (e) {
      return Left(Failure.server(
        message: e.message,
        statusCode: e.statusCode,
      ));
    } on NetworkException catch (e) {
      return Left(Failure.network(message: e.message));
    } on AuthenticationException catch (e) {
      return Left(Failure.authentication(message: e.message));
    } on UnauthorizedException catch (e) {
      return Left(Failure.unauthorized(message: e.message));
    } on TimeoutException catch (e) {
      return Left(Failure.timeout(message: e.message));
    } catch (e) {
      return Left(Failure.unknown(message: '알 수 없는 오류: $e'));
    }
  }

  @override
  Future<Either<Failure, String>> createRoom({
    required List<String> members,
  }) async {
    try {
      final roomId = await _remoteDataSource.createRoom(members);
      return Right(roomId);
    } on ServerException catch (e) {
      return Left(Failure.server(
        message: e.message,
        statusCode: e.statusCode,
      ));
    } on NetworkException catch (e) {
      return Left(Failure.network(message: e.message));
    } on AuthenticationException catch (e) {
      return Left(Failure.authentication(message: e.message));
    } on UnauthorizedException catch (e) {
      return Left(Failure.unauthorized(message: e.message));
    } on TimeoutException catch (e) {
      return Left(Failure.timeout(message: e.message));
    } catch (e) {
      return Left(Failure.unknown(message: '알 수 없는 오류: $e'));
    }
  }

  @override
  Future<Either<Failure, void>> exitRoom({
    required String roomId,
    required String userId,
  }) async {
    try {
      await _remoteDataSource.exitRoom(roomId, userId);
      return const Right(null);
    } on ServerException catch (e) {
      return Left(Failure.server(
        message: e.message,
        statusCode: e.statusCode,
      ));
    } on NetworkException catch (e) {
      return Left(Failure.network(message: e.message));
    } on AuthenticationException catch (e) {
      return Left(Failure.authentication(message: e.message));
    } on UnauthorizedException catch (e) {
      return Left(Failure.unauthorized(message: e.message));
    } on TimeoutException catch (e) {
      return Left(Failure.timeout(message: e.message));
    } catch (e) {
      return Left(Failure.unknown(message: '알 수 없는 오류: $e'));
    }
  }

  @override
  Future<Either<Failure, void>> inviteMember({
    required String roomId,
    required String targetUserId,
    required String senderId,
  }) async {
    try {
      await _remoteDataSource.inviteMember(roomId, targetUserId, senderId);
      return const Right(null);
    } on ServerException catch (e) {
      return Left(Failure.server(
        message: e.message,
        statusCode: e.statusCode,
      ));
    } on NetworkException catch (e) {
      return Left(Failure.network(message: e.message));
    } on AuthenticationException catch (e) {
      return Left(Failure.authentication(message: e.message));
    } on UnauthorizedException catch (e) {
      return Left(Failure.unauthorized(message: e.message));
    } on TimeoutException catch (e) {
      return Left(Failure.timeout(message: e.message));
    } catch (e) {
      return Left(Failure.unknown(message: '알 수 없는 오류: $e'));
    }
  }

  @override
  Future<Either<Failure, List<Message>>> getMessages({
    required String roomId,
    String? lastMessageId,
  }) async {
    try {
      final messages =
          await _remoteDataSource.getMessages(roomId, lastMessageId);
      return Right(messages.map((model) => model.toEntity()).toList());
    } on ServerException catch (e) {
      return Left(Failure.server(
        message: e.message,
        statusCode: e.statusCode,
      ));
    } on NetworkException catch (e) {
      return Left(Failure.network(message: e.message));
    } on AuthenticationException catch (e) {
      return Left(Failure.authentication(message: e.message));
    } on UnauthorizedException catch (e) {
      return Left(Failure.unauthorized(message: e.message));
    } on TimeoutException catch (e) {
      return Left(Failure.timeout(message: e.message));
    } catch (e) {
      return Left(Failure.unknown(message: '알 수 없는 오류: $e'));
    }
  }

  @override
  Future<Either<Failure, void>> sendMessage({
    required String roomId,
    required String messageType,
    String? content,
    Map<String, dynamic>? media,
  }) async {
    try {
      await _webSocketDataSource.sendMessage(
        roomId: roomId,
        messageType: messageType,
        content: content,
        media: media,
      );
      return const Right(null);
    } on WebSocketException catch (e) {
      return Left(Failure.webSocket(message: e.message));
    } catch (e) {
      return Left(Failure.unknown(message: '알 수 없는 오류: $e'));
    }
  }

  @override
  Future<Either<Failure, void>> connectWebSocket(String token) async {
    try {
      await _webSocketDataSource.connect(token);
      return const Right(null);
    } on WebSocketException catch (e) {
      return Left(Failure.webSocket(message: e.message));
    } catch (e) {
      return Left(Failure.unknown(message: '알 수 없는 오류: $e'));
    }
  }

  @override
  Future<Either<Failure, void>> disconnectWebSocket() async {
    try {
      await _webSocketDataSource.disconnect();
      return const Right(null);
    } on WebSocketException catch (e) {
      return Left(Failure.webSocket(message: e.message));
    } catch (e) {
      return Left(Failure.unknown(message: '알 수 없는 오류: $e'));
    }
  }

  @override
  Stream<Message> get messageStream =>
      _webSocketDataSource.messageStream.map((model) => model.toEntity());

  @override
  Stream<bool> get connectionStream => _webSocketDataSource.connectionStream;
}
