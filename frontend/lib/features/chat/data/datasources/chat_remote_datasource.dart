import 'package:dio/dio.dart';

import '../../../../core/constants/api_constants.dart';
import '../../../../core/error/exceptions.dart';
import '../../../../core/network/dio_client.dart';
import '../models/chat_room_model.dart';
import '../models/message_model.dart';

/// Chat API 데이터 소스
abstract class ChatRemoteDataSource {
  Future<List<ChatRoomModel>> getRooms();
  Future<String> createRoom(List<String> members);
  Future<void> exitRoom(String roomId, String userId);
  Future<void> inviteMember(String roomId, String targetUserId, String senderId);
  Future<List<MessageModel>> getMessages(String roomId, String? lastMessageId);
}

class ChatRemoteDataSourceImpl implements ChatRemoteDataSource {
  final DioClient _dioClient;

  ChatRemoteDataSourceImpl({required DioClient dioClient})
      : _dioClient = dioClient;

  @override
  Future<List<ChatRoomModel>> getRooms() async {
    try {
      final response = await _dioClient.get(ApiConstants.chatRooms);

      final data = response.data as Map<String, dynamic>;
      final rooms = data['rooms'] as List<dynamic>;

      return rooms
          .map((room) => ChatRoomModel.fromJson(room as Map<String, dynamic>))
          .toList();
    } on DioException catch (e) {
      throw e.error as Exception;
    } catch (e) {
      throw ServerException(message: '채팅방 목록 조회 실패: $e');
    }
  }

  @override
  Future<String> createRoom(List<String> members) async {
    try {
      final response = await _dioClient.post(
        ApiConstants.chatRooms,
        data: {'members': members},
      );

      final data = response.data as Map<String, dynamic>;
      return data['room_id'] as String;
    } on DioException catch (e) {
      throw e.error as Exception;
    } catch (e) {
      throw ServerException(message: '채팅방 생성 실패: $e');
    }
  }

  @override
  Future<void> exitRoom(String roomId, String userId) async {
    try {
      await _dioClient.delete(
        ApiConstants.chatRooms,
        data: {
          'room_id': roomId,
          'exit_user_id': userId,
        },
      );
    } on DioException catch (e) {
      throw e.error as Exception;
    } catch (e) {
      throw ServerException(message: '채팅방 나가기 실패: $e');
    }
  }

  @override
  Future<void> inviteMember(
    String roomId,
    String targetUserId,
    String senderId,
  ) async {
    try {
      await _dioClient.post(
        ApiConstants.chatRoomMembers(roomId),
        data: {
          'room_id': roomId,
          'target_user_id': targetUserId,
          'sender_id': senderId,
        },
      );
    } on DioException catch (e) {
      throw e.error as Exception;
    } catch (e) {
      throw ServerException(message: '멤버 초대 실패: $e');
    }
  }

  @override
  Future<List<MessageModel>> getMessages(
    String roomId,
    String? lastMessageId,
  ) async {
    try {
      final response = await _dioClient.get(
        ApiConstants.chatRoomMessages(roomId),
        queryParameters: lastMessageId != null
            ? {'last_message_id': lastMessageId}
            : null,
      );

      final data = response.data as Map<String, dynamic>;
      final messages = data['messages'] as List<dynamic>;

      return messages
          .map((msg) => MessageModel.fromJson(msg as Map<String, dynamic>))
          .toList();
    } on DioException catch (e) {
      throw e.error as Exception;
    } catch (e) {
      throw ServerException(message: '메시지 히스토리 조회 실패: $e');
    }
  }
}
