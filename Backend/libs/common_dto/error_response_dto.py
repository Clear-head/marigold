from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """에러 상세 정보"""
    code: str
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "code": "TOKEN_EXPIRED",
                "message": "Token has expired"
            }
        }


class ErrorResponse(BaseModel):
    """에러 응답 (Exception Handler가 반환)"""
    error: ErrorDetail

    class Config:
        json_schema_extra = {
            "example": {
                "error": {
                    "code": "TOKEN_EXPIRED",
                    "message": "Token has expired"
                }
            }
        }