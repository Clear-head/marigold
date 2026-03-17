import 'package:dartz/dartz.dart';

import '../../../../core/error/failures.dart';

abstract class AuthRepository {
  /// 로그인 — POST /auth/tokens
  Future<Either<Failure, Map<String, String>>> login({
    required String userId,
    required String password,
  });

  /// 회원가입 — POST /auth/users
  Future<Either<Failure, void>> signup({
    required String userId,
    required String password,
    required String name,
    required String phone,
    required String birth,
  });

  /// 로그아웃 — DELETE /auth/tokens
  Future<Either<Failure, void>> logout({required String userId});

  /// 토큰 갱신 — PUT /auth/tokens
  Future<Either<Failure, Map<String, String>>> refreshToken({
    required String userId,
    required String refreshToken,
  });
}
