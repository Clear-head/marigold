import 'dart:async';

import '../../../../core/constants/api_constants.dart';
import '../../../../core/error/exceptions.dart';
import '../../../../core/network/websocket_client.dart';
import '../models/message_model.dart';

/// Chat WebSocket 데이터 소스
abstract class ChatWebSocketDataSource {
  Future<void> connect(String token);
  Future<void> disconnect();
  Future<void> sendMessage({
    required String roomId,
    required String messageType,
    String? content,
    Map<String, dynamic>? media,
  });
  Stream<MessageModel> get messageStream;
  Stream<bool> get connectionStream;
}

class ChatWebSocketDataSourceImpl implements ChatWebSocketDataSource {
  final WebSocketClient _webSocketClient;
  final StreamController<MessageModel> _messageController =
      StreamController<MessageModel>.broadcast();
  final StreamController<bool> _connectionController =
      StreamController<bool>.broadcast();

  ChatWebSocketDataSourceImpl({required WebSocketClient webSocketClient})
      : _webSocketClient = webSocketClient {
    _setupListeners();
  }

  /// WebSocket 리스너 설정
  void _setupListeners() {
    // 메시지 수신
    _webSocketClient.messageStream.listen(
      (data) {
        try {
          final type = data['type'] as String?;

          // 채팅 메시지만 파싱
          if (type == ApiConstants.wsEventMessage ||
              type == 'text' ||
              type == 'image' ||
              type == 'video') {
            final message = MessageModel.fromJson(data);
            _messageController.add(message);
          }
        } catch (e) {
          _messageController.addError(
            WebSocketException(message: '메시지 파싱 실패: $e'),
          );
        }
      },
      onError: (error) {
        _messageController.addError(error);
      },
    );

    // 연결 상태 변경
    _webSocketClient.statusStream.listen((status) {
      final isConnected = status == WebSocketStatus.connected;
      _connectionController.add(isConnected);
    });
  }

  @override
  Future<void> connect(String token) async {
    try {
      await _webSocketClient.connect(token);
    } catch (e) {
      throw WebSocketException(message: 'WebSocket 연결 실패: $e');
    }
  }

  @override
  Future<void> disconnect() async {
    try {
      await _webSocketClient.disconnect();
    } catch (e) {
      throw WebSocketException(message: 'WebSocket 연결 해제 실패: $e');
    }
  }

  @override
  Future<void> sendMessage({
    required String roomId,
    required String messageType,
    String? content,
    Map<String, dynamic>? media,
  }) async {
    try {
      final data = <String, dynamic>{
        'type': messageType,
        'room_id': roomId,
        if (content != null) 'content': content,
        if (media != null) 'media': media,
      };

      _webSocketClient.send(data);
    } catch (e) {
      throw WebSocketException(message: '메시지 전송 실패: $e');
    }
  }

  @override
  Stream<MessageModel> get messageStream => _messageController.stream;

  @override
  Stream<bool> get connectionStream => _connectionController.stream;

  void dispose() {
    _messageController.close();
    _connectionController.close();
  }
}
