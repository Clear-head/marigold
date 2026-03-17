// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'media_meta_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$MediaMetaModelImpl _$$MediaMetaModelImplFromJson(Map<String, dynamic> json) =>
    _$MediaMetaModelImpl(
      fileUrl: json['file_url'] as String,
      fileName: json['file_name'] as String,
      fileSize: (json['file_size'] as num).toInt(),
      mimeType: json['mime_type'] as String,
      width: (json['width'] as num?)?.toInt(),
      height: (json['height'] as num?)?.toInt(),
      thumbnailUrl: json['thumbnail_url'] as String?,
      duration: (json['duration'] as num?)?.toDouble(),
    );

Map<String, dynamic> _$$MediaMetaModelImplToJson(
  _$MediaMetaModelImpl instance,
) => <String, dynamic>{
  'file_url': instance.fileUrl,
  'file_name': instance.fileName,
  'file_size': instance.fileSize,
  'mime_type': instance.mimeType,
  'width': instance.width,
  'height': instance.height,
  'thumbnail_url': instance.thumbnailUrl,
  'duration': instance.duration,
};
