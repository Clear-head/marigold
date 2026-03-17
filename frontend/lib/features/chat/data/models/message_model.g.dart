// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'message_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$MessageModelImpl _$$MessageModelImplFromJson(Map<String, dynamic> json) =>
    _$MessageModelImpl(
      id: json['_id'] as String,
      messageType: json['message_type'] as String,
      senderId: json['sender_id'] as String,
      roomId: json['room_id'] as String,
      sendAt: json['send_at'] as String,
      content: json['content'] as String?,
      media: json['media'] == null
          ? null
          : MediaMetaModel.fromJson(json['media'] as Map<String, dynamic>),
    );

Map<String, dynamic> _$$MessageModelImplToJson(_$MessageModelImpl instance) =>
    <String, dynamic>{
      '_id': instance.id,
      'message_type': instance.messageType,
      'sender_id': instance.senderId,
      'room_id': instance.roomId,
      'send_at': instance.sendAt,
      'content': instance.content,
      'media': instance.media,
    };
