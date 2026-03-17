import 'package:dartz/dartz.dart';

import '../../../../core/error/exceptions.dart';
import '../../../../core/error/failures.dart';
import '../../domain/repositories/auth_repository.dart';
import '../datasources/auth_remote_datasource.dart';

class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource _dataSource;

  AuthRepositoryImpl({required AuthRemoteDataSource dataSource})
      : _dataSource = dataSource;

  @override
  Future<Either<Failure, Map<String, String>>> login({
    required String userId,
    required String password,
  }) async {
    try {
      final tokens = await _dataSource.login(userId: userId, password: password);
      return Right(tokens);
    } on AuthenticationException catch (e) {
      return Left(Failure.authentication(message: e.message));
    } on ServerException catch (e) {
      return Left(Failure.server(message: e.message, statusCode: e.statusCode));
    } on NetworkException catch (e) {
      return Left(Failure.network(message: e.message));
    } catch (e) {
      return Left(Failure.unknown(message: '알 수 없는 오류: $e'));
    }
  }

  @override
  Future<Either<Failure, void>> signup({
    required String userId,
    required String password,
    required String name,
    required String phone,
    required String birth,
  }) async {
    try {
      await _dataSource.signup(
        userId: userId,
        password: password,
        name: name,
        phone: phone,
        birth: birth,
      );
      return const Right(null);
    } on ServerException catch (e) {
      return Left(Failure.server(message: e.message, statusCode: e.statusCode));
    } on NetworkException catch (e) {
      return Left(Failure.network(message: e.message));
    } catch (e) {
      return Left(Failure.unknown(message: '알 수 없는 오류: $e'));
    }
  }

  @override
  Future<Either<Failure, void>> logout({required String userId}) async {
    try {
      await _dataSource.logout(userId: userId);
      return const Right(null);
    } on ServerException catch (e) {
      return Left(Failure.server(message: e.message, statusCode: e.statusCode));
    } on NetworkException catch (e) {
      return Left(Failure.network(message: e.message));
    } catch (e) {
      return Left(Failure.unknown(message: '알 수 없는 오류: $e'));
    }
  }

  @override
  Future<Either<Failure, Map<String, String>>> refreshToken({
    required String userId,
    required String refreshToken,
  }) async {
    try {
      final tokens = await _dataSource.refreshToken(
        userId: userId,
        refreshToken: refreshToken,
      );
      return Right(tokens);
    } on AuthenticationException catch (e) {
      return Left(Failure.authentication(message: e.message));
    } on ServerException catch (e) {
      return Left(Failure.server(message: e.message, statusCode: e.statusCode));
    } on NetworkException catch (e) {
      return Left(Failure.network(message: e.message));
    } catch (e) {
      return Left(Failure.unknown(message: '알 수 없는 오류: $e'));
    }
  }
}
