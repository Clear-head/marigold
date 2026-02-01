# Backend\servers\auth\api\auth_router.py
# fastapi

# 비밀번호만 인증하는 라우터가 필요함

from fastapi import APIRouter, status, Header, Depends, HTTPException
from dto.dto import LoginRequest, TokenResponse, SignupRequest, LoginResponse
from typing import Annotated

from services.auth_service import IssueJWTService
from services.login_service import login

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/tokens", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def login_endpoint(request: LoginRequest):
    """
    Login (Create Tokens)
    """
    # 1. 로그인 검증 (ID/PW)
    await login(request.user_id, request.password)
    
    # 2. 토큰 발급
    auth_service = IssueJWTService()
    tokens = await auth_service.issue_tokens(request.user_id)
    
    return LoginResponse(access_token=tokens[f"access_token_{request.user_id}"], refresh_token=tokens[f"refresh_token_{request.user_id}"])

@router.delete("/tokens", status_code=status.HTTP_204_NO_CONTENT)
async def logout_endpoint(user_id: str): 
    pass

@router.put("/tokens", response_model=TokenResponse)
async def refresh_token_endpoint(
    user_id: str,
    authorization: Annotated[str | None, Header()] = None
):
    """
    Refresh Tokens
    Header: Authorization: Bearer {refresh_token}
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    refresh_token = authorization.split(" ")[1]
    
    auth_service = IssueJWTService()
    new_tokens = await auth_service.refresh_token(user_id, refresh_token)
    
    return TokenResponse(access_token=new_tokens[f"access_token_{user_id}"], refresh_token=new_tokens[f"refresh_token_{user_id}"])

@router.post("/users", status_code=status.HTTP_201_CREATED)
async def signup_endpoint(request: SignupRequest):
    pass

@router.delete("/users", status_code=status.HTTP_204_NO_CONTENT)
async def withdraw_endpoint(user_id: str):
    pass
