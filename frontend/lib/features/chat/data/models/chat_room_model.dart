import 'package:freezed_annotation/freezed_annotation.dart';

import '../../domain/entities/chat_room.dart';

part 'chat_room_model.freezed.dart';
part 'chat_room_model.g.dart';

/// ChatRoom DTO (JSON 직렬화)
@freezed
class ChatRoomModel with _$ChatRoomModel {
  const factory ChatRoomModel({
    @JsonKey(name: 'id') required String id,
    required List<String> members,
  }) = _ChatRoomModel;

  const ChatRoomModel._();

  factory ChatRoomModel.fromJson(Map<String, dynamic> json) =>
      _$ChatRoomModelFromJson(json);

  /// Entity로 변환
  ChatRoom toEntity() {
    return ChatRoom(
      id: id,
      members: members,
    );
  }

  /// Entity에서 변환
  factory ChatRoomModel.fromEntity(ChatRoom entity) {
    return ChatRoomModel(
      id: entity.id,
      members: entity.members,
    );
  }
}
