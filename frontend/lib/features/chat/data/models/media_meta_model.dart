import 'package:freezed_annotation/freezed_annotation.dart';

import '../../domain/entities/media_meta.dart';

part 'media_meta_model.freezed.dart';
part 'media_meta_model.g.dart';

/// MediaMeta DTO (JSON 직렬화)
@freezed
class MediaMetaModel with _$MediaMetaModel {
  const factory MediaMetaModel({
    @JsonKey(name: 'file_url') required String fileUrl,
    @JsonKey(name: 'file_name') required String fileName,
    @JsonKey(name: 'file_size') required int fileSize,
    @JsonKey(name: 'mime_type') required String mimeType,
    int? width,
    int? height,
    @JsonKey(name: 'thumbnail_url') String? thumbnailUrl,
    double? duration,
  }) = _MediaMetaModel;

  const MediaMetaModel._();

  factory MediaMetaModel.fromJson(Map<String, dynamic> json) =>
      _$MediaMetaModelFromJson(json);

  /// Entity로 변환
  MediaMeta toEntity() {
    return MediaMeta(
      fileUrl: fileUrl,
      fileName: fileName,
      fileSize: fileSize,
      mimeType: mimeType,
      width: width,
      height: height,
      thumbnailUrl: thumbnailUrl,
      duration: duration,
    );
  }

  /// Entity에서 변환
  factory MediaMetaModel.fromEntity(MediaMeta entity) {
    return MediaMetaModel(
      fileUrl: entity.fileUrl,
      fileName: entity.fileName,
      fileSize: entity.fileSize,
      mimeType: entity.mimeType,
      width: entity.width,
      height: entity.height,
      thumbnailUrl: entity.thumbnailUrl,
      duration: entity.duration,
    );
  }
}
