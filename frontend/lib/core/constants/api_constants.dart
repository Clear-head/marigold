import 'package:flutter_dotenv/flutter_dotenv.dart';

/// API 상수 정의
/// .env 파일에서 환경별 URL 로드, 나머지는 앱 상수
class ApiConstants {
  // Base URLs
  static String get authBaseUrl => dotenv.get('AUTH_BASE_URL');
  static String get chatBaseUrl => dotenv.get('CHAT_BASE_URL');
  static String get userBaseUrl => dotenv.get('USER_BASE_URL');
  static String get notificationBaseUrl => dotenv.get('NOTIFICATION_BASE_URL');
  static String get calendarBaseUrl => dotenv.get('CALENDAR_BASE_URL');
  static String get aiBaseUrl => dotenv.get('AI_BASE_URL');

  // WebSocket (.env에서 로드)
  static String get chatWebSocketUrl => dotenv.get('CHAT_WEBSOCKET_URL');

  // Chat API Endpoints
  static const String chatRooms = '/api/chat/rooms';
  static String chatRoomMessages(String roomId) =>
      '/api/chat/rooms/$roomId/messages';
  static String chatRoomMembers(String roomId) =>
      '/api/chat/rooms/$roomId/members';
  static String chatWebSocket(String token) => '/ws/chat?token=$token';

  // Auth API Endpoints (auth_router.py 기반)
  static const String authTokens = '/auth/tokens';
  static const String authUsers = '/auth/users';

  // Timeouts
  static const Duration connectTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);
  static const Duration sendTimeout = Duration(seconds: 30);

  // Headers
  static const String authorizationHeader = 'Authorization';
  static const String contentTypeHeader = 'Content-Type';
  static const String applicationJson = 'application/json';

  // JWT
  static const String jwtAlgorithm = 'HS256';
  static const String jwtIssuer = 'marigold-chat-server';
  static const int accessTokenExpireMinutes = 60;
  static const int refreshTokenExpireMinutes = 600;

  // WebSocket Events
  static const String wsEventConnectionEstablished = 'connection_established';
  static const String wsEventPing = 'ping';
  static const String wsEventPong = 'pong';
  static const String wsEventError = 'error';
  static const String wsEventMessage = 'message';

  // Message Types (Backend MessageTypeEnum)
  static const String messageTypeText = 'text';
  static const String messageTypeImage = 'image';
  static const String messageTypeVideo = 'video';

  // Pagination
  static const int defaultPageSize = 20;
}
