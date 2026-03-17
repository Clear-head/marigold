import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:logger/logger.dart';

/// JWT 토큰을 안전하게 저장하고 관리하는 클래스
class TokenStorage {
  final FlutterSecureStorage _storage;
  final Logger _logger;

  static const String _accessTokenKey = 'access_token';
  static const String _refreshTokenKey = 'refresh_token';
  static const String _userIdKey = 'user_id';

  TokenStorage({
    FlutterSecureStorage? storage,
    Logger? logger,
  })  : _storage = storage ?? const FlutterSecureStorage(),
        _logger = logger ?? Logger();

  /// Access Token 저장
  Future<void> saveAccessToken(String token) async {
    try {
      await _storage.write(key: _accessTokenKey, value: token);
      _logger.d('Access token saved');
    } catch (e) {
      _logger.e('Failed to save access token: $e');
      rethrow;
    }
  }

  /// Refresh Token 저장
  Future<void> saveRefreshToken(String token) async {
    try {
      await _storage.write(key: _refreshTokenKey, value: token);
      _logger.d('Refresh token saved');
    } catch (e) {
      _logger.e('Failed to save refresh token: $e');
      rethrow;
    }
  }

  /// User ID 저장
  Future<void> saveUserId(String userId) async {
    try {
      await _storage.write(key: _userIdKey, value: userId);
      _logger.d('User ID saved');
    } catch (e) {
      _logger.e('Failed to save user ID: $e');
      rethrow;
    }
  }

  /// Access Token 가져오기
  Future<String?> getAccessToken() async {
    try {
      return await _storage.read(key: _accessTokenKey);
    } catch (e) {
      _logger.e('Failed to get access token: $e');
      return null;
    }
  }

  /// Refresh Token 가져오기
  Future<String?> getRefreshToken() async {
    try {
      return await _storage.read(key: _refreshTokenKey);
    } catch (e) {
      _logger.e('Failed to get refresh token: $e');
      return null;
    }
  }

  /// User ID 가져오기
  Future<String?> getUserId() async {
    try {
      return await _storage.read(key: _userIdKey);
    } catch (e) {
      _logger.e('Failed to get user ID: $e');
      return null;
    }
  }

  /// 인증 여부 확인
  Future<bool> isAuthenticated() async {
    final accessToken = await getAccessToken();
    return accessToken != null && accessToken.isNotEmpty;
  }

  /// 모든 토큰 삭제 (로그아웃)
  Future<void> clearAll() async {
    try {
      await _storage.delete(key: _accessTokenKey);
      await _storage.delete(key: _refreshTokenKey);
      await _storage.delete(key: _userIdKey);
      _logger.d('All tokens cleared');
    } catch (e) {
      _logger.e('Failed to clear tokens: $e');
      rethrow;
    }
  }

  /// 모든 저장소 데이터 삭제
  Future<void> deleteAll() async {
    try {
      await _storage.deleteAll();
      _logger.d('All storage cleared');
    } catch (e) {
      _logger.e('Failed to clear storage: $e');
      rethrow;
    }
  }
}
