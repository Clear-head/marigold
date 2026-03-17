// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'media_meta.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

/// @nodoc
mixin _$MediaMeta {
  String get fileUrl => throw _privateConstructorUsedError;
  String get fileName => throw _privateConstructorUsedError;
  int get fileSize => throw _privateConstructorUsedError; // bytes
  String get mimeType => throw _privateConstructorUsedError;
  int? get width => throw _privateConstructorUsedError;
  int? get height => throw _privateConstructorUsedError;
  String? get thumbnailUrl => throw _privateConstructorUsedError;
  double? get duration => throw _privateConstructorUsedError;

  /// Create a copy of MediaMeta
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $MediaMetaCopyWith<MediaMeta> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $MediaMetaCopyWith<$Res> {
  factory $MediaMetaCopyWith(MediaMeta value, $Res Function(MediaMeta) then) =
      _$MediaMetaCopyWithImpl<$Res, MediaMeta>;
  @useResult
  $Res call({
    String fileUrl,
    String fileName,
    int fileSize,
    String mimeType,
    int? width,
    int? height,
    String? thumbnailUrl,
    double? duration,
  });
}

/// @nodoc
class _$MediaMetaCopyWithImpl<$Res, $Val extends MediaMeta>
    implements $MediaMetaCopyWith<$Res> {
  _$MediaMetaCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of MediaMeta
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? fileUrl = null,
    Object? fileName = null,
    Object? fileSize = null,
    Object? mimeType = null,
    Object? width = freezed,
    Object? height = freezed,
    Object? thumbnailUrl = freezed,
    Object? duration = freezed,
  }) {
    return _then(
      _value.copyWith(
            fileUrl: null == fileUrl
                ? _value.fileUrl
                : fileUrl // ignore: cast_nullable_to_non_nullable
                      as String,
            fileName: null == fileName
                ? _value.fileName
                : fileName // ignore: cast_nullable_to_non_nullable
                      as String,
            fileSize: null == fileSize
                ? _value.fileSize
                : fileSize // ignore: cast_nullable_to_non_nullable
                      as int,
            mimeType: null == mimeType
                ? _value.mimeType
                : mimeType // ignore: cast_nullable_to_non_nullable
                      as String,
            width: freezed == width
                ? _value.width
                : width // ignore: cast_nullable_to_non_nullable
                      as int?,
            height: freezed == height
                ? _value.height
                : height // ignore: cast_nullable_to_non_nullable
                      as int?,
            thumbnailUrl: freezed == thumbnailUrl
                ? _value.thumbnailUrl
                : thumbnailUrl // ignore: cast_nullable_to_non_nullable
                      as String?,
            duration: freezed == duration
                ? _value.duration
                : duration // ignore: cast_nullable_to_non_nullable
                      as double?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$MediaMetaImplCopyWith<$Res>
    implements $MediaMetaCopyWith<$Res> {
  factory _$$MediaMetaImplCopyWith(
    _$MediaMetaImpl value,
    $Res Function(_$MediaMetaImpl) then,
  ) = __$$MediaMetaImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String fileUrl,
    String fileName,
    int fileSize,
    String mimeType,
    int? width,
    int? height,
    String? thumbnailUrl,
    double? duration,
  });
}

/// @nodoc
class __$$MediaMetaImplCopyWithImpl<$Res>
    extends _$MediaMetaCopyWithImpl<$Res, _$MediaMetaImpl>
    implements _$$MediaMetaImplCopyWith<$Res> {
  __$$MediaMetaImplCopyWithImpl(
    _$MediaMetaImpl _value,
    $Res Function(_$MediaMetaImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of MediaMeta
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? fileUrl = null,
    Object? fileName = null,
    Object? fileSize = null,
    Object? mimeType = null,
    Object? width = freezed,
    Object? height = freezed,
    Object? thumbnailUrl = freezed,
    Object? duration = freezed,
  }) {
    return _then(
      _$MediaMetaImpl(
        fileUrl: null == fileUrl
            ? _value.fileUrl
            : fileUrl // ignore: cast_nullable_to_non_nullable
                  as String,
        fileName: null == fileName
            ? _value.fileName
            : fileName // ignore: cast_nullable_to_non_nullable
                  as String,
        fileSize: null == fileSize
            ? _value.fileSize
            : fileSize // ignore: cast_nullable_to_non_nullable
                  as int,
        mimeType: null == mimeType
            ? _value.mimeType
            : mimeType // ignore: cast_nullable_to_non_nullable
                  as String,
        width: freezed == width
            ? _value.width
            : width // ignore: cast_nullable_to_non_nullable
                  as int?,
        height: freezed == height
            ? _value.height
            : height // ignore: cast_nullable_to_non_nullable
                  as int?,
        thumbnailUrl: freezed == thumbnailUrl
            ? _value.thumbnailUrl
            : thumbnailUrl // ignore: cast_nullable_to_non_nullable
                  as String?,
        duration: freezed == duration
            ? _value.duration
            : duration // ignore: cast_nullable_to_non_nullable
                  as double?,
      ),
    );
  }
}

/// @nodoc

class _$MediaMetaImpl implements _MediaMeta {
  const _$MediaMetaImpl({
    required this.fileUrl,
    required this.fileName,
    required this.fileSize,
    required this.mimeType,
    this.width,
    this.height,
    this.thumbnailUrl,
    this.duration,
  });

  @override
  final String fileUrl;
  @override
  final String fileName;
  @override
  final int fileSize;
  // bytes
  @override
  final String mimeType;
  @override
  final int? width;
  @override
  final int? height;
  @override
  final String? thumbnailUrl;
  @override
  final double? duration;

  @override
  String toString() {
    return 'MediaMeta(fileUrl: $fileUrl, fileName: $fileName, fileSize: $fileSize, mimeType: $mimeType, width: $width, height: $height, thumbnailUrl: $thumbnailUrl, duration: $duration)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$MediaMetaImpl &&
            (identical(other.fileUrl, fileUrl) || other.fileUrl == fileUrl) &&
            (identical(other.fileName, fileName) ||
                other.fileName == fileName) &&
            (identical(other.fileSize, fileSize) ||
                other.fileSize == fileSize) &&
            (identical(other.mimeType, mimeType) ||
                other.mimeType == mimeType) &&
            (identical(other.width, width) || other.width == width) &&
            (identical(other.height, height) || other.height == height) &&
            (identical(other.thumbnailUrl, thumbnailUrl) ||
                other.thumbnailUrl == thumbnailUrl) &&
            (identical(other.duration, duration) ||
                other.duration == duration));
  }

  @override
  int get hashCode => Object.hash(
    runtimeType,
    fileUrl,
    fileName,
    fileSize,
    mimeType,
    width,
    height,
    thumbnailUrl,
    duration,
  );

  /// Create a copy of MediaMeta
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$MediaMetaImplCopyWith<_$MediaMetaImpl> get copyWith =>
      __$$MediaMetaImplCopyWithImpl<_$MediaMetaImpl>(this, _$identity);
}

abstract class _MediaMeta implements MediaMeta {
  const factory _MediaMeta({
    required final String fileUrl,
    required final String fileName,
    required final int fileSize,
    required final String mimeType,
    final int? width,
    final int? height,
    final String? thumbnailUrl,
    final double? duration,
  }) = _$MediaMetaImpl;

  @override
  String get fileUrl;
  @override
  String get fileName;
  @override
  int get fileSize; // bytes
  @override
  String get mimeType;
  @override
  int? get width;
  @override
  int? get height;
  @override
  String? get thumbnailUrl;
  @override
  double? get duration;

  /// Create a copy of MediaMeta
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$MediaMetaImplCopyWith<_$MediaMetaImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
