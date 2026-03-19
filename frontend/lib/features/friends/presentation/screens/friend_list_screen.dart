import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../user/domain/entities/user_info.dart';
import '../../../user/presentation/providers/user_providers.dart';
import 'user_search_screen.dart';

class FriendListScreen extends ConsumerWidget {
  const FriendListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final friendsAsync = ref.watch(friendListProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('친구'),
        actions: [
          IconButton(
            icon: const Icon(Icons.person_search_outlined),
            tooltip: '친구 찾기',
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const UserSearchScreen()),
            ),
          ),
        ],
      ),
      body: friendsAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.error_outline, size: 48, color: Colors.red),
              const SizedBox(height: 12),
              Text('친구 목록을 불러오지 못했습니다.\n$e',
                  textAlign: TextAlign.center,
                  style: const TextStyle(color: Colors.grey)),
              const SizedBox(height: 16),
              TextButton(
                onPressed: () => ref.invalidate(friendListProvider),
                child: const Text('다시 시도'),
              ),
            ],
          ),
        ),
        data: (friends) => friends.isEmpty
            ? const Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.people_outline, size: 64, color: Colors.grey),
                    SizedBox(height: 16),
                    Text('친구가 없습니다',
                        style: TextStyle(fontSize: 16, color: Colors.grey)),
                    SizedBox(height: 8),
                    Text('상단 검색 버튼으로 친구를 추가해 보세요',
                        style: TextStyle(fontSize: 13, color: Colors.grey)),
                  ],
                ),
              )
            : ListView.builder(
                itemCount: friends.length,
                itemBuilder: (context, index) {
                  return _FriendTile(user: friends[index]);
                },
              ),
      ),
    );
  }
}

class _FriendTile extends ConsumerWidget {
  final UserInfo user;

  const _FriendTile({required this.user});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return ListTile(
      leading: CircleAvatar(child: Text(user.name[0])),
      title: Text(user.name),
      subtitle: Text(user.userId),
      onLongPress: () => _showActionSheet(context, ref),
    );
  }

  void _showActionSheet(BuildContext context, WidgetRef ref) {
    showModalBottomSheet(
      context: context,
      builder: (_) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              leading: const Icon(Icons.person_remove_outlined),
              title: const Text('친구 삭제'),
              onTap: () async {
                Navigator.pop(context);
                final success = await ref
                    .read(friendActionProvider.notifier)
                    .deleteFriend(user.userId);
                if (context.mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text(
                        success ? '${user.name}님을 친구에서 삭제했습니다.' : '친구 삭제에 실패했습니다.',
                      ),
                    ),
                  );
                }
              },
            ),
            ListTile(
              leading: const Icon(Icons.block, color: Colors.red),
              title: const Text('차단', style: TextStyle(color: Colors.red)),
              onTap: () async {
                Navigator.pop(context);
                final success = await ref
                    .read(friendActionProvider.notifier)
                    .blockUser(user.userId);
                if (context.mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text(
                        success ? '${user.name}님을 차단했습니다.' : '차단에 실패했습니다.',
                      ),
                    ),
                  );
                }
              },
            ),
          ],
        ),
      ),
    );
  }
}
