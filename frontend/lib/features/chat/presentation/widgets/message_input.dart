import 'package:flutter/material.dart';

/// 메시지 입력 위젯
class MessageInput extends StatefulWidget {
  final Function(String) onSend;

  const MessageInput({
    super.key,
    required this.onSend,
  });

  @override
  State<MessageInput> createState() => _MessageInputState();
}

class _MessageInputState extends State<MessageInput> {
  final TextEditingController _controller = TextEditingController();
  bool _canSend = false;

  @override
  void initState() {
    super.initState();
    _controller.addListener(_updateCanSend);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _updateCanSend() {
    final canSend = _controller.text.trim().isNotEmpty;
    if (canSend != _canSend) {
      setState(() {
        _canSend = canSend;
      });
    }
  }

  void _handleSend() {
    final text = _controller.text.trim();
    if (text.isEmpty) return;

    widget.onSend(text);
    _controller.clear();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
      decoration: BoxDecoration(
        color: Theme.of(context).scaffoldBackgroundColor,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 4,
            offset: const Offset(0, -2),
          ),
        ],
      ),
      child: SafeArea(
        child: Row(
          children: [
            // 추가 기능 버튼 (이미지, 비디오 등)
            IconButton(
              icon: const Icon(Icons.add_circle_outline),
              onPressed: () {
                // TODO: 미디어 선택 기능
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('미디어 전송 기능 (구현 예정)')),
                );
              },
            ),

            // 텍스트 입력 필드
            Expanded(
              child: TextField(
                controller: _controller,
                decoration: InputDecoration(
                  hintText: '메시지를 입력하세요',
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(24),
                    borderSide: BorderSide.none,
                  ),
                  filled: true,
                  fillColor: Colors.grey[200],
                  contentPadding: const EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 10,
                  ),
                ),
                maxLines: null,
                textInputAction: TextInputAction.newline,
                onSubmitted: (_) => _handleSend(),
              ),
            ),

            const SizedBox(width: 8),

            // 전송 버튼
            CircleAvatar(
              backgroundColor: _canSend ? Colors.deepPurple : Colors.grey[300],
              child: IconButton(
                icon: Icon(
                  Icons.send,
                  color: _canSend ? Colors.white : Colors.grey[500],
                  size: 20,
                ),
                onPressed: _canSend ? _handleSend : null,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
