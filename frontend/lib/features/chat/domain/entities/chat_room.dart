import 'package:freezed_annotation/freezed_annotation.dart';

part 'chat_room.freezed.dart';

/// 채팅방 엔티티 (Backend ChatRoom과 동일)
@freezed
class ChatRoom with _$ChatRoom {
  const factory ChatRoom({
    required String id,
    required List<String> members, // user IDs
  }) = _ChatRoom;
}
