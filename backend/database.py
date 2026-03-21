import os
from supabase import create_client, Client

SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

def get_supabase_client() -> Client:
    """Supabase 클라이언트 인스턴스 반환 함수"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)
