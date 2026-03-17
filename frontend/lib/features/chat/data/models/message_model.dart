import 'package:freezed_annotation/freezed_annotation.dart';

import '../../domain/entities/message.dart';
import '../../domain/entities/message_type.dart';
import 'media_meta_model.dart';

part 'message_model.freezed.dart';
part 'message_model.g.dart';

/// Message DTO (JSON 직렬화)
@freezed
class MessageModel with _$MessageModel {
  const factory MessageModel({
    @JsonKey(name: '_id') required String id,
    @JsonKey(name: 'message_type') required String messageType,
    @JsonKey(name: 'sender_id') required String senderId,
    @JsonKey(name: 'room_id') required String roomId,
    @JsonKey(name: 'send_at') required String sendAt,
    String? content,
    MediaMetaModel? media,
  }) = _MessageModel;

  const MessageModel._();

  factory MessageModel.fromJson(Map<String, dynamic> json) =>
      _$MessageModelFromJson(json);

  /// Entity로 변환
  Message toEntity() {
    return Message(
      id: id,
      messageType: MessageType.fromString(messageType),
      senderId: senderId,
      roomId: roomId,
      sendAt: DateTime.parse(sendAt),
      content: content,
      media: media?.toEntity(),
    );
  }

  /// Entity에서 변환
  factory MessageModel.fromEntity(Message entity) {
    return MessageModel(
      id: entity.id,
      messageType: entity.messageType.value,
      senderId: entity.senderId,
      roomId: entity.roomId,
      sendAt: entity.sendAt.toIso8601String(),
      content: entity.content,
      media: entity.media != null
          ? MediaMetaModel.fromEntity(entity.media!)
          : null,
    );
  }
}
