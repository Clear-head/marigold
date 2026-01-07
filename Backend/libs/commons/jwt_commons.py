
#   jwt 만들기
async def create_jwt_token():
    """

    jwt 엑세스 토큰이랑 리프레시토큰 2개 만들어서 리턴

    # Access Token Payload
    access_payload = {
        "userId": user_id,
        "exp": access_exp, -> .env
        "iat": now_timestamp,
        "iss": "marigold-chat-server",
        "type": "access"
    }

    # Refresh Token Payload
    refresh_payload = {
        "userId": user_id,
        "exp": refresh_exp, -> .env
        "iat": now_timestamp,
        "iss": "marigold-chat-server",
        "type": "refresh"
    }

    :return: jwt 2개
    """

    pass

#   토큰 검사 HTTP 용
async def verify_jwt_token_http(token):
    pass

#   토큰 검사 websocket 용 -> 석훈이가 할꺼
async def verify_jwt_token_websocket(token):
    pass

#   엑세스 토큰 만료시 리프레시 토큰 받고 갱신
async def refresh_access_token():
    pass