from fastapi import Request
from fastapi.responses import JSONResponse

from commons.logger import get_marigold_logger
from exceptions.auth_exceptions import AuthException

logger = get_marigold_logger("auth-exception-handler")


async def auth_exception_handler(request: Request, exc: AuthException):
    """
    AuthException 전용 핸들러

    모든 인증/인가 에러를 일관된 형식으로 반환합니다.
    """
    logger.warning(
        f"Auth exception: {exc.error_code} - {exc.detail} "
        f"[path: {request.url.path}, method: {request.method}]"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.detail
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    일반 예외 핸들러

    예상하지 못한 에러를 처리합니다.
    """
    logger.error(
        f"Unexpected error: {str(exc)} "
        f"[path: {request.url.path}, method: {request.method}]",
        exc_info=True
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred"
            }
        }
    )