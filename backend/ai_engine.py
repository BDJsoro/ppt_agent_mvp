import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# 최신 google-genai SDK 사용. 환경 변수에서 GEMINI_API_KEY 로드
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class Slide(BaseModel):
    title: str = Field(description="슬라이드의 핵심 제목 (10자 내외)")
    content: list[str] = Field(description="슬라이드의 본문 내용 (개조식 요약 문장 배열, 3~5줄)")

class Presentation(BaseModel):
    topic: str = Field(description="오탈자가 교정된 깔끔한 전체 프레젠테이션 주제명")
    slides: list[Slide] = Field(description="정확히 요구된 장수만큼 분할된 슬라이드 배열")

def generate_ppt_content(topic: str, slide_count: int = 8) -> dict:
    """
    주어진 주제와 슬라이드 장수를 입력받아, 제미나이 리서치를 거친 구조화된 JSON 도출
    """
    # 엣지 케이스 방어: 너무 많은 슬라이드 생성 요청 제한 (최대 15장)
    if slide_count > 15:
        slide_count = 15
    elif slide_count < 1:
        slide_count = 1
        
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")

    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""
    당신은 글로벌 탑 티어 비즈니스 컨설턴트이자 파워포인트 제작의 장인입니다.
    사용자가 제시한 주제에 대해 깊이 있는 리서치와 논리적 구조화를 진행하세요.
    사용자가 요청한 슬라이드 장수({slide_count}장)는 '오직 본문 슬라이드의 개수'를 의미합니다. 표지는 별도입니다.
    최종 결과물은 전체 프레젠테이션 주제명(topic) 1개와, 이를 뒷받침하는 총 {slide_count}개의 본문 슬라이드(slides 배열)로 정확하고 완벽하게 구성되어야 합니다.
    각 슬라이드는 간결하고 임팩트 있는 '제목'과, 핵심만 전달하는 3~5개의 짧은 '본문 문장(개조식, ~함, ~음 형태 종결)'을 가져야 합니다.
    장황한 서술어를 금지합니다.
    
    주제: "{topic}"
    목표 본문 슬라이드 개수: {slide_count}개
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Presentation,
            temperature=0.7, # 창의성과 논리성의 적절한 조화
        ),
    )
    
    # JSON 문자열을 파이썬 딕셔너리로 변환하여 반환
    return json.loads(response.text)
