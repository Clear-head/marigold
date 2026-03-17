// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'message.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

/// @nodoc
mixin _$Message {
  String get id => throw _privateConstructorUsedError;
  MessageType get messageType => throw _privateConstructorUsedError;
  String get senderId => throw _privateConstructorUsedError;
  String get roomId => throw _privateConstructorUsedError;
  DateTime get sendAt => throw _privateConstructorUsedError;
  String? get content => throw _privateConstructorUsedError; // TEXT 전용
  MediaMeta? get media => throw _privateConstructorUsedError;

  /// Create a copy of Message
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $MessageCopyWith<Message> get copyWith => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $MessageCopyWith<$Res> {
  factory $MessageCopyWith(Message value, $Res Function(Message) then) =
      _$MessageCopyWithImpl<$Res, Message>;
  @useResult
  $Res call({
    String id,
    MessageType messageType,
    String senderId,
    String roomId,
    DateTime sendAt,
    String? content,
    MediaMeta? media,
  });

  $MediaMetaCopyWith<$Res>? get media;
}

/// @nodoc
class _$MessageCopyWithImpl<$Res, $Val extends Message>
    implements $MessageCopyWith<$Res> {
  _$MessageCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of Message
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? messageType = null,
    Object? senderId = null,
    Object? roomId = null,
    Object? sendAt = null,
    Object? content = freezed,
    Object? media = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as String,
            messageType: null == messageType
                ? _value.messageType
                : messageType // ignore: cast_nullable_to_non_nullable
                      as MessageType,
            senderId: null == senderId
                ? _value.senderId
                : senderId // ignore: cast_nullable_to_non_nullable
                      as String,
            roomId: null == roomId
                ? _value.roomId
                : roomId // ignore: cast_nullable_to_non_nullable
                      as String,
            sendAt: null == sendAt
                ? _value.sendAt
                : sendAt // ignore: cast_nullable_to_non_nullable
                      as DateTime,
            content: freezed == content
                ? _value.content
                : content // ignore: cast_nullable_to_non_nullable
                      as String?,
            media: freezed == media
                ? _value.media
                : media // ignore: cast_nullable_to_non_nullable
                      as MediaMeta?,
          )
          as $Val,
    );
  }

  /// Create a copy of Message
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $MediaMetaCopyWith<$Res>? get media {
    if (_value.media == null) {
      return null;
    }

    return $MediaMetaCopyWith<$Res>(_value.media!, (value) {
      return _then(_value.copyWith(media: value) as $Val);
    });
  }
}

/// @nodoc
abstract class _$$MessageImplCopyWith<$Res> implements $MessageCopyWith<$Res> {
  factory _$$MessageImplCopyWith(
    _$MessageImpl value,
    $Res Function(_$MessageImpl) then,
  ) = __$$MessageImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String id,
    MessageType messageType,
    String senderId,
    String roomId,
    DateTime sendAt,
    String? content,
    MediaMeta? media,
  });

  @override
  $MediaMetaCopyWith<$Res>? get media;
}

/// @nodoc
class __$$MessageImplCopyWithImpl<$Res>
    extends _$MessageCopyWithImpl<$Res, _$MessageImpl>
    implements _$$MessageImplCopyWith<$Res> {
  __$$MessageImplCopyWithImpl(
    _$MessageImpl _value,
    $Res Function(_$MessageImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of Message
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? messageType = null,
    Object? senderId = null,
    Object? roomId = null,
    Object? sendAt = null,
    Object? content = freezed,
    Object? media = freezed,
  }) {
    return _then(
      _$MessageImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as String,
        messageType: null == messageType
            ? _value.messageType
            : messageType // ignore: cast_nullable_to_non_nullable
                  as MessageType,
        senderId: null == senderId
            ? _value.senderId
            : senderId // ignore: cast_nullable_to_non_nullable
                  as String,
        roomId: null == roomId
            ? _value.roomId
            : roomId // ignore: cast_nullable_to_non_nullable
                  as String,
        sendAt: null == sendAt
            ? _value.sendAt
            : sendAt // ignore: cast_nullable_to_non_nullable
                  as DateTime,
        content: freezed == content
            ? _value.content
            : content // ignore: cast_nullable_to_non_nullable
                  as String?,
        media: freezed == media
            ? _value.media
            : media // ignore: cast_nullable_to_non_nullable
                  as MediaMeta?,
      ),
    );
  }
}

/// @nodoc

class _$MessageImpl extends _Message {
  const _$MessageImpl({
    required this.id,
    required this.messageType,
    required this.senderId,
    required this.roomId,
    required this.sendAt,
    this.content,
    this.media,
  }) : super._();

  @override
  final String id;
  @override
  final MessageType messageType;
  @override
  final String senderId;
  @override
  final String roomId;
  @override
  final DateTime sendAt;
  @override
  final String? content;
  // TEXT 전용
  @override
  final MediaMeta? media;

  @override
  String toString() {
    return 'Message(id: $id, messageType: $messageType, senderId: $senderId, roomId: $roomId, sendAt: $sendAt, content: $content, media: $media)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$MessageImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.messageType, messageType) ||
                other.messageType == messageType) &&
            (identical(other.senderId, senderId) ||
                other.senderId == senderId) &&
            (identical(other.roomId, roomId) || other.roomId == roomId) &&
            (identical(other.sendAt, sendAt) || other.sendAt == sendAt) &&
            (identical(other.content, content) || other.content == content) &&
            (identical(other.media, media) || other.media == media));
  }

  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    messageType,
    senderId,
    roomId,
    sendAt,
    content,
    media,
  );

  /// Create a copy of Message
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$MessageImplCopyWith<_$MessageImpl> get copyWith =>
      __$$MessageImplCopyWithImpl<_$MessageImpl>(this, _$identity);
}

abstract class _Message extends Message {
  const factory _Message({
    required final String id,
    required final MessageType messageType,
    required final String senderId,
    required final String roomId,
    required final DateTime sendAt,
    final String? content,
    final MediaMeta? media,
  }) = _$MessageImpl;
  const _Message._() : super._();

  @override
  String get id;
  @override
  MessageType get messageType;
  @override
  String get senderId;
  @override
  String get roomId;
  @override
  DateTime get sendAt;
  @override
  String? get content; // TEXT 전용
  @override
  MediaMeta? get media;

  /// Create a copy of Message
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$MessageImplCopyWith<_$MessageImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
