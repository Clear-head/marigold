import 'package:dio/dio.dart';

import '../../../../core/constants/api_constants.dart';
import '../../../../core/error/exceptions.dart';
import '../../../../core/network/dio_client.dart';

abstract class AuthRemoteDataSource {
  Future<Map<String, String>> login({
    required String userId,
    required String password,
  });

  Future<void> signup({
    required String userId,
    required String password,
    required String name,
    required String phone,
    required String birth,
  });

  Future<void> logout({required String userId});

  Future<Map<String, String>> refreshToken({
    required String userId,
    required String refreshToken,
  });
}

class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  final DioClient _dioClient;

  AuthRemoteDataSourceImpl({required DioClient dioClient})
      : _dioClient = dioClient;

  @override
  Future<Map<String, String>> login({
    required String userId,
    required String password,
  }) async {
    try {
      final response = await _dioClient.post(
        ApiConstants.authTokens,
        data: {'user_id': userId, 'password': password},
      );
      final data = response.data as Map<String, dynamic>;
      return {
        'access_token': data['access_token'] as String,
        'refresh_token': data['refresh_token'] as String,
      };
    } on DioException catch (e) {
      throw e.error as Exception;
    } catch (e) {
      throw ServerException(message: '로그인 실패: $e');
    }
  }

  @override
  Future<void> signup({
    required String userId,
    required String password,
    required String name,
    required String phone,
    required String birth,
  }) async {
    try {
      final now = DateTime.now().toUtc().toIso8601String();
      await _dioClient.post(
        ApiConstants.authUsers,
        data: {
          'user_id': userId,
          'password': password,
          'name': name,
          'phone': phone,
          'birth': birth,
          'created_at': now,
        },
      );
    } on DioException catch (e) {
      throw e.error as Exception;
    } catch (e) {
      throw ServerException(message: '회원가입 실패: $e');
    }
  }

  @override
  Future<void> logout({required String userId}) async {
    try {
      await _dioClient.delete(
        '${ApiConstants.authTokens}?user_id=$userId',
      );
    } on DioException catch (e) {
      throw e.error as Exception;
    } catch (e) {
      throw ServerException(message: '로그아웃 실패: $e');
    }
  }

  @override
  Future<Map<String, String>> refreshToken({
    required String userId,
    required String refreshToken,
  }) async {
    try {
      final response = await _dioClient.put(
        '${ApiConstants.authTokens}?user_id=$userId',
        options: Options(headers: {'Authorization': 'Bearer $refreshToken'}),
      );
      final data = response.data as Map<String, dynamic>;
      return {
        'access_token': data['access_token'] as String,
        'refresh_token': data['refresh_token'] as String,
      };
    } on DioException catch (e) {
      throw e.error as Exception;
    } catch (e) {
      throw ServerException(message: '토큰 갱신 실패: $e');
    }
  }
}
