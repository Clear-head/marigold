class AuthException(Exception):
    """인증/인가 관련 기본 예외 클래스"""

    def __init__(self, detail: str, error_code: str, status_code: int = 401):
        """
        Args:
            detail: 사람이 읽을 수 있는 에러 메시지
            error_code: 프로그램이 처리할 수 있는 에러 코드 (SCREAMING_SNAKE_CASE)
            status_code: HTTP 상태 코드
        """
        self.detail = detail
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(detail)


# ==================== 토큰 검증 관련 (401) ====================

class InvalidTokenException(AuthException):
    """토큰 검증 실패 (변조, 서명 불일치, 형식 오류 등)"""

    def __init__(self, detail: str = "Invalid token"):
        super().__init__(
            detail=detail,
            error_code="TOKEN_INVALID",
            status_code=401
        )


class TokenExpiredException(AuthException):
    """토큰 만료"""

    def __init__(self, detail: str = "Token has expired"):
        super().__init__(
            detail=detail,
            error_code="TOKEN_EXPIRED",
            status_code=401
        )


class InvalidTokenTypeException(AuthException):
    """잘못된 토큰 타입 (Access를 기대했는데 Refresh가 옴)"""

    def __init__(self, expected: str = None, received: str = None):
        if expected and received:
            detail = f"Expected {expected} token, but received {received} token"
        else:
            detail = "Invalid token type"

        super().__init__(
            detail=detail,
            error_code="TOKEN_TYPE_INVALID",
            status_code=401
        )


# ==================== 세션 관련 (401) ====================

class TokenRevokedException(AuthException):
    """토큰이 무효화됨 (로그아웃, 강제 로그아웃 등)"""

    def __init__(self, detail: str = "Token has been revoked"):
        super().__init__(
            detail=detail,
            error_code="TOKEN_REVOKED",
            status_code=401
        )


class NoActiveSessionException(AuthException):
    """활성 세션이 없음 (2단계 검증 실패)"""

    def __init__(self, detail: str = "No active session found"):
        super().__init__(
            detail=detail,
            error_code="NO_ACTIVE_SESSION",
            status_code=401
        )


# ==================== 기기/권한 제한 (403) ====================

class MaxDevicesExceededException(AuthException):
    """최대 기기 수 초과"""

    def __init__(self, max_devices: int = 3):
        super().__init__(
            detail=f"Maximum number of devices ({max_devices}) exceeded",
            error_code="MAX_DEVICES_EXCEEDED",
            status_code=403
        )


# ==================== 인프라 에러 (500) ====================

class RedisConnectionException(AuthException):
    """Redis 연결 실패"""

    def __init__(self, detail: str = "Redis connection error"):
        super().__init__(
            detail=detail,
            error_code="REDIS_CONNECTION_ERROR",
            status_code=500
        )