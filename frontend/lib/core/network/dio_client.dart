import 'package:dio/dio.dart';
import 'package:logger/logger.dart';

import '../constants/api_constants.dart';
import '../error/exceptions.dart';
import '../storage/token_storage.dart';

/// Dio HTTP 클라이언트
/// JWT 인터셉터, 에러 핸들링, 로깅 포함
class DioClient {
  late final Dio _dio;
  final TokenStorage _tokenStorage;
  final Logger _logger;

  DioClient({
    required TokenStorage tokenStorage,
    Logger? logger,
    String? baseUrl,
  })  : _tokenStorage = tokenStorage,
        _logger = logger ?? Logger() {
    _dio = Dio(
      BaseOptions(
        baseUrl: baseUrl ?? ApiConstants.chatBaseUrl,
        connectTimeout: ApiConstants.connectTimeout,
        receiveTimeout: ApiConstants.receiveTimeout,
        sendTimeout: ApiConstants.sendTimeout,
        headers: {
          ApiConstants.contentTypeHeader: ApiConstants.applicationJson,
        },
      ),
    );

    _dio.interceptors.addAll([
      _jwtInterceptor(),
      _loggingInterceptor(),
      _errorInterceptor(),
    ]);
  }

  /// Dio 인스턴스 접근
  Dio get dio => _dio;

  /// JWT 인터셉터
  /// 모든 요청에 Authorization 헤더 추가
  Interceptor _jwtInterceptor() {
    return InterceptorsWrapper(
      onRequest: (options, handler) async {
        final token = await _tokenStorage.getAccessToken();

        if (token != null && token.isNotEmpty) {
          options.headers[ApiConstants.authorizationHeader] = 'Bearer $token';
          _logger.d('JWT token added to request');
        }

        return handler.next(options);
      },
      onError: (error, handler) async {
        // 401 Unauthorized - 토큰 갱신 시도
        if (error.response?.statusCode == 401) {
          _logger.w('401 Unauthorized - attempting token refresh');

          try {
            final refreshToken = await _tokenStorage.getRefreshToken();
            final userId = await _tokenStorage.getUserId();

            if (refreshToken == null || userId == null) {
              _logger.e('No refresh token or userId available');
              await _tokenStorage.clearAll();
              return handler.reject(error);
            }

            // 인터셉터 없는 별도 Dio로 갱신 요청 (무한 루프 방지)
            final refreshDio = Dio(BaseOptions(baseUrl: ApiConstants.authBaseUrl));
            final response = await refreshDio.put(
              '${ApiConstants.authTokens}?user_id=$userId',
              options: Options(
                headers: {ApiConstants.authorizationHeader: 'Bearer $refreshToken'},
              ),
            );

            final data = response.data as Map<String, dynamic>;
            final newAccessToken = data['access_token'] as String;
            final newRefreshToken = data['refresh_token'] as String;

            await _tokenStorage.saveAccessToken(newAccessToken);
            await _tokenStorage.saveRefreshToken(newRefreshToken);

            _logger.i('Token refreshed successfully');

            // 원래 요청 재시도 (인터셉터가 저장소에서 새 토큰을 읽어서 헤더에 추가)
            final retryResponse = await _dio.fetch(error.requestOptions);
            return handler.resolve(retryResponse);
          } catch (e) {
            _logger.e('Token refresh failed: $e');
            await _tokenStorage.clearAll();
            return handler.reject(error);
          }
        }

        return handler.next(error);
      },
    );
  }

  /// 로깅 인터셉터
  Interceptor _loggingInterceptor() {
    return InterceptorsWrapper(
      onRequest: (options, handler) {
        _logger.d('''
🌐 REQUEST
├─ Method: ${options.method}
├─ URL: ${options.uri}
├─ Headers: ${options.headers}
└─ Data: ${options.data}
        ''');
        return handler.next(options);
      },
      onResponse: (response, handler) {
        _logger.d('''
✅ RESPONSE
├─ Status: ${response.statusCode}
├─ URL: ${response.requestOptions.uri}
└─ Data: ${response.data}
        ''');
        return handler.next(response);
      },
      onError: (error, handler) {
        _logger.e('''
❌ ERROR
├─ Status: ${error.response?.statusCode}
├─ URL: ${error.requestOptions.uri}
├─ Message: ${error.message}
└─ Data: ${error.response?.data}
        ''');
        return handler.next(error);
      },
    );
  }

  /// 에러 핸들링 인터셉터
  Interceptor _errorInterceptor() {
    return InterceptorsWrapper(
      onError: (error, handler) {
        final exception = _handleDioError(error);

        return handler.reject(
          DioException(
            requestOptions: error.requestOptions,
            response: error.response,
            type: error.type,
            error: exception,
            message: exception.toString(),
          ),
        );
      },
    );
  }

  /// Dio 에러를 Custom Exception으로 변환
  Exception _handleDioError(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return TimeoutException(
          message: '요청 시간이 초과되었습니다',
        );

      case DioExceptionType.badResponse:
        final statusCode = error.response?.statusCode;
        final message = error.response?.data?['message'] ?? '서버 오류가 발생했습니다';

        if (statusCode == 401) {
          return AuthenticationException(message: message);
        } else if (statusCode == 403) {
          return UnauthorizedException(message: message);
        } else if (statusCode == 404) {
          return ServerException(
            message: '요청한 리소스를 찾을 수 없습니다',
            statusCode: statusCode,
          );
        } else if (statusCode != null && statusCode >= 500) {
          return ServerException(
            message: message,
            statusCode: statusCode,
          );
        }

        return ServerException(
          message: message,
          statusCode: statusCode,
          data: error.response?.data,
        );

      case DioExceptionType.cancel:
        return NetworkException(message: '요청이 취소되었습니다');

      case DioExceptionType.connectionError:
      case DioExceptionType.badCertificate:
      case DioExceptionType.unknown:
        return NetworkException(
          message: '네트워크 연결을 확인해주세요',
        );
    }
  }

  /// GET 요청
  Future<Response<T>> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      return await _dio.get<T>(
        path,
        queryParameters: queryParameters,
        options: options,
      );
    } on DioException {
      rethrow;
    }
  }

  /// POST 요청
  Future<Response<T>> post<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      return await _dio.post<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
      );
    } on DioException {
      rethrow;
    }
  }

  /// PUT 요청
  Future<Response<T>> put<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      return await _dio.put<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
      );
    } on DioException {
      rethrow;
    }
  }

  /// DELETE 요청
  Future<Response<T>> delete<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      return await _dio.delete<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
      );
    } on DioException {
      rethrow;
    }
  }

  /// Base URL 변경
  void setBaseUrl(String baseUrl) {
    _dio.options.baseUrl = baseUrl;
  }
}
