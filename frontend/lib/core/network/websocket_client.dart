import 'dart:async';
import 'dart:convert';

import 'package:logger/logger.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

import '../constants/api_constants.dart';
import '../error/exceptions.dart';

/// WebSocket 연결 상태
enum WebSocketStatus {
  connecting,
  connected,
  disconnected,
  error,
}

/// WebSocket 클라이언트
/// Backend의 Heartbeat (Ping/Pong) 메커니즘 구현
class WebSocketClient {
  WebSocketChannel? _channel;
  final Logger _logger;

  WebSocketStatus _status = WebSocketStatus.disconnected;
  Timer? _heartbeatTimer;
  Timer? _reconnectTimer;
  int _reconnectAttempts = 0;
  String? _lastToken;

  static const int _maxReconnectAttempts = 5;
  static const Duration _reconnectDelay = Duration(seconds: 3);
  static const Duration _heartbeatInterval = Duration(seconds: 30);

  final StreamController<Map<String, dynamic>> _messageController =
      StreamController<Map<String, dynamic>>.broadcast();
  final StreamController<WebSocketStatus> _statusController =
      StreamController<WebSocketStatus>.broadcast();
  final StreamController<void> _unauthorizedController =
      StreamController<void>.broadcast();

  WebSocketClient({Logger? logger}) : _logger = logger ?? Logger();

  /// WebSocket 연결 상태 스트림
  Stream<WebSocketStatus> get statusStream => _statusController.stream;

  /// 메시지 수신 스트림
  Stream<Map<String, dynamic>> get messageStream => _messageController.stream;

  /// 세션 만료 스트림 (로그인 화면으로 이동 트리거)
  Stream<void> get unauthorizedStream => _unauthorizedController.stream;

  /// 현재 연결 상태
  WebSocketStatus get status => _status;

  /// 연결 여부
  bool get isConnected => _status == WebSocketStatus.connected;

  /// WebSocket 연결 (token: JWT access token)
  Future<void> connect(String token) async {
    if (_status == WebSocketStatus.connected ||
        _status == WebSocketStatus.connecting) {
      _logger.w('Already connected or connecting');
      return;
    }

    _lastToken = token;

    try {
      _updateStatus(WebSocketStatus.connecting);

      final url = Uri.parse(
        '${ApiConstants.chatWebSocketUrl}${ApiConstants.chatWebSocket(token)}',
      );

      _logger.i('Connecting to WebSocket: $url');

      _channel = WebSocketChannel.connect(url);

      // 연결 성공
      _updateStatus(WebSocketStatus.connected);
      _reconnectAttempts = 0;
      _logger.i('WebSocket connected');

      // 메시지 수신 리스닝
      _channel!.stream.listen(
        _onMessage,
        onError: _onError,
        onDone: _onDone,
        cancelOnError: false,
      );

      // Heartbeat 시작
      _startHeartbeat();
    } catch (e) {
      _logger.e('WebSocket connection failed: $e');
      _updateStatus(WebSocketStatus.error);
      _scheduleReconnect(token);
    }
  }

  /// 메시지 수신 핸들러
  void _onMessage(dynamic message) {
    try {
      final data = jsonDecode(message as String) as Map<String, dynamic>;
      final type = data['type'] as String?;

      _logger.d('WebSocket message received: $type');

      // Ping 메시지 처리
      if (type == ApiConstants.wsEventPing) {
        _sendPong();
        return;
      }

      // 연결 확인 메시지
      if (type == ApiConstants.wsEventConnectionEstablished) {
        _logger.i('Connection established: ${data['message']}');
        return;
      }

      // 에러 메시지
      if (type == ApiConstants.wsEventError) {
        _logger.e('WebSocket error message: ${data['message']}');
        _messageController.addError(
          WebSocketException(message: data['message'] as String? ?? 'Unknown error'),
        );
        return;
      }

      // 세션 만료 메시지
      if (type == 'session_expired') {
        _logger.w('Session expired: ${data['message']}');
        _unauthorizedController.add(null);
        return;
      }

      // 일반 메시지를 스트림에 추가
      _messageController.add(data);
    } catch (e) {
      _logger.e('Failed to parse message: $e');
    }
  }

  /// 에러 핸들러
  void _onError(dynamic error) {
    _logger.e('WebSocket error: $error');
    _updateStatus(WebSocketStatus.error);
  }

  /// 연결 종료 핸들러
  void _onDone() {
    _logger.w('WebSocket connection closed');
    _updateStatus(WebSocketStatus.disconnected);
    _stopHeartbeat();
  }

  /// Heartbeat 시작
  void _startHeartbeat() {
    _heartbeatTimer?.cancel();
    _heartbeatTimer = Timer.periodic(_heartbeatInterval, (_) {
      // 서버가 자동으로 ping을 보내므로, 여기서는 연결 체크만 수행
      if (_status != WebSocketStatus.connected) {
        _logger.w('Heartbeat check: not connected');
        _stopHeartbeat();
      }
    });
    _logger.d('Heartbeat started');
  }

  /// Heartbeat 중지
  void _stopHeartbeat() {
    _heartbeatTimer?.cancel();
    _heartbeatTimer = null;
    _logger.d('Heartbeat stopped');
  }

  /// Pong 응답 전송 (서버의 Ping에 대한 응답)
  void _sendPong() {
    send({
      'type': ApiConstants.wsEventPong,
      'timestamp': DateTime.now().millisecondsSinceEpoch,
    });
    _logger.d('Pong sent');
  }

  /// 재연결 스케줄링
  void _scheduleReconnect(String token) {
    if (_reconnectAttempts >= _maxReconnectAttempts) {
      _logger.e('Max reconnect attempts reached');
      return;
    }

    _reconnectAttempts++;
    _logger.i('Scheduling reconnect attempt $_reconnectAttempts/$_maxReconnectAttempts');

    _reconnectTimer?.cancel();
    _reconnectTimer = Timer(_reconnectDelay, () {
      _logger.i('Attempting to reconnect...');
      connect(token);
    });
  }

  /// 메시지 전송
  void send(Map<String, dynamic> data) {
    if (!isConnected) {
      _logger.w('Cannot send message: not connected');
      throw WebSocketException(message: 'WebSocket is not connected');
    }

    try {
      final message = jsonEncode(data);
      _channel!.sink.add(message);
      _logger.d('Message sent: ${data['type']}');
    } catch (e) {
      _logger.e('Failed to send message: $e');
      throw WebSocketException(message: 'Failed to send message: $e');
    }
  }

  /// 연결 상태 업데이트
  void _updateStatus(WebSocketStatus status) {
    _status = status;
    _statusController.add(status);
    _logger.d('WebSocket status changed: $status');
  }

  /// 연결 종료
  Future<void> disconnect() async {
    _logger.i('Disconnecting WebSocket');

    _stopHeartbeat();
    _reconnectTimer?.cancel();
    _reconnectTimer = null;

    await _channel?.sink.close();
    _channel = null;

    _updateStatus(WebSocketStatus.disconnected);
  }

  /// 리소스 정리
  Future<void> dispose() async {
    await disconnect();
    await _messageController.close();
    await _statusController.close();
    await _unauthorizedController.close();
  }
}
