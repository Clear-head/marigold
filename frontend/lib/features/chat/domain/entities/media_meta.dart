import 'package:freezed_annotation/freezed_annotation.dart';

part 'media_meta.freezed.dart';

/// 미디어 메타데이터 (Backend MediaMeta와 동일)
@freezed
class MediaMeta with _$MediaMeta {
  const factory MediaMeta({
    required String fileUrl,
    required String fileName,
    required int fileSize, // bytes
    required String mimeType,
    int? width,
    int? height,
    String? thumbnailUrl,
    double? duration, // VIDEO 전용 (초)
  }) = _MediaMeta;
}
