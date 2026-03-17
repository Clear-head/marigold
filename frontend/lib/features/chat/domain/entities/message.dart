import 'package:freezed_annotation/freezed_annotation.dart';

import 'media_meta.dart';
import 'message_type.dart';

part 'message.freezed.dart';

/// 메시지 엔티티 (Backend MessageDTO와 동일)
@freezed
class Message with _$Message {
  const factory Message({
    required String id,
    required MessageType messageType,
    required String senderId,
    required String roomId,
    required DateTime sendAt,
    String? content, // TEXT 전용
    MediaMeta? media, // IMAGE, VIDEO 전용
  }) = _Message;

  const Message._();

  /// 텍스트 메시지 여부
  bool get isText => messageType == MessageType.text;

  /// 이미지 메시지 여부
  bool get isImage => messageType == MessageType.image;

  /// 비디오 메시지 여부
  bool get isVideo => messageType == MessageType.video;

  /// 미디어 메시지 여부
  bool get hasMedia => media != null;
}
