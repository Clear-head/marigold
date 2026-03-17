/// 메시지 타입 (Backend MessageTypeEnum과 동일)
enum MessageType {
  text('text'),
  image('image'),
  video('video');

  const MessageType(this.value);
  final String value;

  static MessageType fromString(String value) {
    return MessageType.values.firstWhere(
      (type) => type.value == value,
      orElse: () => MessageType.text,
    );
  }
}
