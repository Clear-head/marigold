import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/providers/core_providers.dart';
import '../../data/datasources/auth_remote_datasource.dart';
import '../../data/repositories/auth_repository_impl.dart';
import '../../domain/repositories/auth_repository.dart';

final authRemoteDataSourceProvider = Provider<AuthRemoteDataSource>((ref) {
  final dioClient = ref.watch(authDioClientProvider);
  return AuthRemoteDataSourceImpl(dioClient: dioClient);
});

final authRepositoryProvider = Provider<AuthRepository>((ref) {
  final dataSource = ref.watch(authRemoteDataSourceProvider);
  return AuthRepositoryImpl(dataSource: dataSource);
});

/// 로그인 상태 — AsyncNotifier
class LoginNotifier extends AsyncNotifier<void> {
  @override
  Future<void> build() async {}

  Future<bool> login(String userId, String password) async {
    state = const AsyncLoading();
    final repository = ref.read(authRepositoryProvider);
    final tokenStorage = ref.read(tokenStorageProvider);

    final result = await repository.login(userId: userId, password: password);

    return result.fold(
      (failure) {
        state = AsyncError(failure.toString(), StackTrace.current);
        return false;
      },
      (tokens) async {
        await tokenStorage.saveAccessToken(tokens['access_token']!);
        await tokenStorage.saveRefreshToken(tokens['refresh_token']!);
        await tokenStorage.saveUserId(userId);
        state = const AsyncData(null);
        return true;
      },
    );
  }
}

final loginProvider = AsyncNotifierProvider<LoginNotifier, void>(LoginNotifier.new);

/// 회원가입 — AsyncNotifier
class SignupNotifier extends AsyncNotifier<void> {
  @override
  Future<void> build() async {}

  Future<bool> signup({
    required String userId,
    required String password,
    required String name,
    required String phone,
    required String birth,
  }) async {
    state = const AsyncLoading();
    final repository = ref.read(authRepositoryProvider);

    final result = await repository.signup(
      userId: userId,
      password: password,
      name: name,
      phone: phone,
      birth: birth,
    );

    return result.fold(
      (failure) {
        state = AsyncError(failure.toString(), StackTrace.current);
        return false;
      },
      (_) {
        state = const AsyncData(null);
        return true;
      },
    );
  }
}

final signupProvider = AsyncNotifierProvider<SignupNotifier, void>(SignupNotifier.new);

/// 로그아웃
final logoutProvider = FutureProvider.autoDispose<void>((ref) async {
  final tokenStorage = ref.read(tokenStorageProvider);
  final userId = await tokenStorage.getUserId();
  if (userId != null) {
    final repository = ref.read(authRepositoryProvider);
    await repository.logout(userId: userId);
  }
  await tokenStorage.clearAll();
});
