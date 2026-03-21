from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import get_supabase_client

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Supabase JWT 토큰 검증 의존성 (FastAPI Dependency)
    프론트엔드에서 전달받은 Bearer 토큰의 유효성을 파악하고 유저 객체를 반환.
    """
    token = credentials.credentials
    supabase = get_supabase_client()
    
    # 토큰을 사용하여 유저 세션/정보 조회 시도
    user_response = supabase.auth.get_user(token)
    
    if not user_response or not user_response.user:
        raise HTTPException(
            status_code=401,
            detail="유효하지 않은 인증 토큰입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_response.user
