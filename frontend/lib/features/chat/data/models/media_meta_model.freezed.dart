// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'media_meta_model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

MediaMetaModel _$MediaMetaModelFromJson(Map<String, dynamic> json) {
  return _MediaMetaModel.fromJson(json);
}

/// @nodoc
mixin _$MediaMetaModel {
  @JsonKey(name: 'file_url')
  String get fileUrl => throw _privateConstructorUsedError;
  @JsonKey(name: 'file_name')
  String get fileName => throw _privateConstructorUsedError;
  @JsonKey(name: 'file_size')
  int get fileSize => throw _privateConstructorUsedError;
  @JsonKey(name: 'mime_type')
  String get mimeType => throw _privateConstructorUsedError;
  int? get width => throw _privateConstructorUsedError;
  int? get height => throw _privateConstructorUsedError;
  @JsonKey(name: 'thumbnail_url')
  String? get thumbnailUrl => throw _privateConstructorUsedError;
  double? get duration => throw _privateConstructorUsedError;

  /// Serializes this MediaMetaModel to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of MediaMetaModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $MediaMetaModelCopyWith<MediaMetaModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $MediaMetaModelCopyWith<$Res> {
  factory $MediaMetaModelCopyWith(
    MediaMetaModel value,
    $Res Function(MediaMetaModel) then,
  ) = _$MediaMetaModelCopyWithImpl<$Res, MediaMetaModel>;
  @useResult
  $Res call({
    @JsonKey(name: 'file_url') String fileUrl,
    @JsonKey(name: 'file_name') String fileName,
    @JsonKey(name: 'file_size') int fileSize,
    @JsonKey(name: 'mime_type') String mimeType,
    int? width,
    int? height,
    @JsonKey(name: 'thumbnail_url') String? thumbnailUrl,
    double? duration,
  });
}

/// @nodoc
class _$MediaMetaModelCopyWithImpl<$Res, $Val extends MediaMetaModel>
    implements $MediaMetaModelCopyWith<$Res> {
  _$MediaMetaModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of MediaMetaModel
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
abstract class _$$MediaMetaModelImplCopyWith<$Res>
    implements $MediaMetaModelCopyWith<$Res> {
  factory _$$MediaMetaModelImplCopyWith(
    _$MediaMetaModelImpl value,
    $Res Function(_$MediaMetaModelImpl) then,
  ) = __$$MediaMetaModelImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    @JsonKey(name: 'file_url') String fileUrl,
    @JsonKey(name: 'file_name') String fileName,
    @JsonKey(name: 'file_size') int fileSize,
    @JsonKey(name: 'mime_type') String mimeType,
    int? width,
    int? height,
    @JsonKey(name: 'thumbnail_url') String? thumbnailUrl,
    double? duration,
  });
}

/// @nodoc
class __$$MediaMetaModelImplCopyWithImpl<$Res>
    extends _$MediaMetaModelCopyWithImpl<$Res, _$MediaMetaModelImpl>
    implements _$$MediaMetaModelImplCopyWith<$Res> {
  __$$MediaMetaModelImplCopyWithImpl(
    _$MediaMetaModelImpl _value,
    $Res Function(_$MediaMetaModelImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of MediaMetaModel
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
      _$MediaMetaModelImpl(
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
@JsonSerializable()
class _$MediaMetaModelImpl extends _MediaMetaModel {
  const _$MediaMetaModelImpl({
    @JsonKey(name: 'file_url') required this.fileUrl,
    @JsonKey(name: 'file_name') required this.fileName,
    @JsonKey(name: 'file_size') required this.fileSize,
    @JsonKey(name: 'mime_type') required this.mimeType,
    this.width,
    this.height,
    @JsonKey(name: 'thumbnail_url') this.thumbnailUrl,
    this.duration,
  }) : super._();

  factory _$MediaMetaModelImpl.fromJson(Map<String, dynamic> json) =>
      _$$MediaMetaModelImplFromJson(json);

  @override
  @JsonKey(name: 'file_url')
  final String fileUrl;
  @override
  @JsonKey(name: 'file_name')
  final String fileName;
  @override
  @JsonKey(name: 'file_size')
  final int fileSize;
  @override
  @JsonKey(name: 'mime_type')
  final String mimeType;
  @override
  final int? width;
  @override
  final int? height;
  @override
  @JsonKey(name: 'thumbnail_url')
  final String? thumbnailUrl;
  @override
  final double? duration;

  @override
  String toString() {
    return 'MediaMetaModel(fileUrl: $fileUrl, fileName: $fileName, fileSize: $fileSize, mimeType: $mimeType, width: $width, height: $height, thumbnailUrl: $thumbnailUrl, duration: $duration)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$MediaMetaModelImpl &&
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

  @JsonKey(includeFromJson: false, includeToJson: false)
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

  /// Create a copy of MediaMetaModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$MediaMetaModelImplCopyWith<_$MediaMetaModelImpl> get copyWith =>
      __$$MediaMetaModelImplCopyWithImpl<_$MediaMetaModelImpl>(
        this,
        _$identity,
      );

  @override
  Map<String, dynamic> toJson() {
    return _$$MediaMetaModelImplToJson(this);
  }
}

abstract class _MediaMetaModel extends MediaMetaModel {
  const factory _MediaMetaModel({
    @JsonKey(name: 'file_url') required final String fileUrl,
    @JsonKey(name: 'file_name') required final String fileName,
    @JsonKey(name: 'file_size') required final int fileSize,
    @JsonKey(name: 'mime_type') required final String mimeType,
    final int? width,
    final int? height,
    @JsonKey(name: 'thumbnail_url') final String? thumbnailUrl,
    final double? duration,
  }) = _$MediaMetaModelImpl;
  const _MediaMetaModel._() : super._();

  factory _MediaMetaModel.fromJson(Map<String, dynamic> json) =
      _$MediaMetaModelImpl.fromJson;

  @override
  @JsonKey(name: 'file_url')
  String get fileUrl;
  @override
  @JsonKey(name: 'file_name')
  String get fileName;
  @override
  @JsonKey(name: 'file_size')
  int get fileSize;
  @override
  @JsonKey(name: 'mime_type')
  String get mimeType;
  @override
  int? get width;
  @override
  int? get height;
  @override
  @JsonKey(name: 'thumbnail_url')
  String? get thumbnailUrl;
  @override
  double? get duration;

  /// Create a copy of MediaMetaModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$MediaMetaModelImplCopyWith<_$MediaMetaModelImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
