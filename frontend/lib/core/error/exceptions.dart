/// 예외 클래스 정의 (Data Layer)
library;

class ServerException implements Exception {
  final String message;
  final int? statusCode;
  final Map<String, dynamic>? data;

  ServerException({
    required this.message,
    this.statusCode,
    this.data,
  });

  @override
  String toString() =>
      'ServerException(message: $message, statusCode: $statusCode)';
}

class NetworkException implements Exception {
  final String message;

  NetworkException({required this.message});

  @override
  String toString() => 'NetworkException(message: $message)';
}

class AuthenticationException implements Exception {
  final String message;

  AuthenticationException({required this.message});

  @override
  String toString() => 'AuthenticationException(message: $message)';
}

class UnauthorizedException implements Exception {
  final String message;

  UnauthorizedException({required this.message});

  @override
  String toString() => 'UnauthorizedException(message: $message)';
}

class CacheException implements Exception {
  final String message;

  CacheException({required this.message});

  @override
  String toString() => 'CacheException(message: $message)';
}

class TimeoutException implements Exception {
  final String message;

  TimeoutException({required this.message});

  @override
  String toString() => 'TimeoutException(message: $message)';
}

class WebSocketException implements Exception {
  final String message;

  WebSocketException({required this.message});

  @override
  String toString() => 'WebSocketException(message: $message)';
}
