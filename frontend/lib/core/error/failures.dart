import 'package:freezed_annotation/freezed_annotation.dart';

part 'failures.freezed.dart';

/// 실패 타입 정의
@freezed
class Failure with _$Failure {
  const factory Failure.server({
    required String message,
    int? statusCode,
  }) = ServerFailure;

  const factory Failure.network({
    required String message,
  }) = NetworkFailure;

  const factory Failure.authentication({
    required String message,
  }) = AuthenticationFailure;

  const factory Failure.unauthorized({
    required String message,
  }) = UnauthorizedFailure;

  const factory Failure.notFound({
    required String message,
  }) = NotFoundFailure;

  const factory Failure.validation({
    required String message,
    Map<String, dynamic>? errors,
  }) = ValidationFailure;

  const factory Failure.cache({
    required String message,
  }) = CacheFailure;

  const factory Failure.timeout({
    required String message,
  }) = TimeoutFailure;

  const factory Failure.webSocket({
    required String message,
  }) = WebSocketFailure;

  const factory Failure.unknown({
    required String message,
  }) = UnknownFailure;
}
