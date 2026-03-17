import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/providers/core_providers.dart';
import '../../domain/entities/message.dart';
import '../providers/chat_providers.dart';
import '../widgets/message_bubble.dart';
import '../widgets/message_input.dart';

/// 채팅방 화면
class ChatRoomScreen extends ConsumerStatefulWidget {
  final String roomId;
  final String roomName;

  const ChatRoomScreen({
    super.key,
    required this.roomId,
    required this.roomName,
  });

  @override
  ConsumerState<ChatRoomScreen> createState() => _ChatRoomScreenState();
}

class _ChatRoomScreenState extends ConsumerState<ChatRoomScreen> {
  final ScrollController _scrollController = ScrollController();
  final List<Message> _messages = [];
  String? _currentUserId;

  @override
  void initState() {
    super.initState();
    _loadMessages();
    _listenToRealtimeMessages();
    _loadCurrentUserId();
  }

  Future<void> _loadCurrentUserId() async {
    final tokenStorage = ref.read(tokenStorageProvider);
    _currentUserId = await tokenStorage.getUserId();
    setState(() {});
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  /// 초기 메시지 로드
  void _loadMessages() {
    ref.read(chatMessagesProvider(widget.roomId).future).then((messages) {
      setState(() {
        _messages.clear();
        _messages.addAll(messages);
      });
      _scrollToBottom();
    }).catchError((e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('메시지를 불러오지 못했습니다: $e')),
        );
        Navigator.of(context).pop();
      }
    });
  }

  /// 실시간 메시지 리스닝
  void _listenToRealtimeMessages() {
    ref.listen<AsyncValue<Message>>(realtimeMessagesProvider, (_, next) {
      next.whenData((message) {
        if (message.roomId == widget.roomId) {
          setState(() {
            _messages.add(message);
          });
          _scrollToBottom();
        }
      });
    });
  }

  /// 스크롤을 맨 아래로
  void _scrollToBottom() {
    if (_scrollController.hasClients) {
      Future.delayed(const Duration(milliseconds: 100), () {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      });
    }
  }

  /// 메시지 전송
  Future<void> _sendMessage(String content) async {
    final repository = ref.read(chatRepositoryProvider);
    final result = await repository.sendMessage(
      roomId: widget.roomId,
      messageType: 'text',
      content: content,
    );

    result.fold(
      (failure) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('메시지 전송 실패: ${failure.toString()}')),
          );
        }
      },
      (_) {
        // 성공 - WebSocket을 통해 실시간으로 메시지가 수신됨
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final connectionStatus = ref.watch(chatConnectionStatusProvider);

    return Scaffold(
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(widget.roomName),
            connectionStatus.when(
              data: (isConnected) => Text(
                isConnected ? '연결됨' : '연결 끊김',
                style: TextStyle(
                  fontSize: 12,
                  color: isConnected ? Colors.green : Colors.red,
                ),
              ),
              loading: () => const Text(
                '연결 중...',
                style: TextStyle(fontSize: 12, color: Colors.orange),
              ),
              error: (_, __) => const Text(
                '오류',
                style: TextStyle(fontSize: 12, color: Colors.red),
              ),
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.more_vert),
            onPressed: () {
              // TODO: 채팅방 설정
            },
          ),
        ],
      ),
      body: Column(
        children: [
          // 메시지 목록
          Expanded(
            child: _messages.isEmpty
                ? const Center(
                    child: Text(
                      '메시지가 없습니다',
                      style: TextStyle(color: Colors.grey),
                    ),
                  )
                : ListView.builder(
                    controller: _scrollController,
                    padding: const EdgeInsets.all(16),
                    itemCount: _messages.length,
                    itemBuilder: (context, index) {
                      final message = _messages[index];
                      final isMe = _currentUserId != null &&
                          message.senderId == _currentUserId;

                      return MessageBubble(
                        message: message,
                        isMe: isMe,
                      );
                    },
                  ),
          ),

          // 메시지 입력창
          MessageInput(
            onSend: _sendMessage,
          ),
        ],
      ),
    );
  }
}
