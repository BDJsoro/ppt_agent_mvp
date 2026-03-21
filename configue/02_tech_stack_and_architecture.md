# 기술 스택 및 아키텍처 (Tech Stack & Architecture)

## 1. 프론트엔드 (Frontend)
- **Framework:** Next.js (React 기반, 빠른 빌드와 라우팅)
- **Styling:** Tailwind CSS + UI 라이브러리 (shadcn/ui 추천)
  - **선정 이유:** 트렌디한 모던 UI/UX(글래스모피즘 등) 구현이 용이하며, 비동기 상태바(로딩 중 UI)를 세련되게 작성하기 좋음.

## 2. 백엔드 (Backend & API)
- **Framework:** Python FastAPI
- **PPT 라이브러리:** `python-pptx`
  - **선정 이유:** Python 생태계가 AI 도구 연동에 가장 유리하며, `python-pptx`는 바이너리 파일 조작, 폰트 텍스트 매핑, 그리고 **숨겨진 문서 메타데이터(속성) 삽입**에 있어 가장 안정적인 도구임.
- **Task Queue (비동기 처리):** Celery + Redis (또는 설계 규모에 따라 범용 백그라운드 워커)
  - **선정 이유:** 50명 동시 생성 대기열을 관리하여 서버 다운 방지.

## 3. AI 및 리서치 엔진
- **LLM:** Google Gemini API
- **Tools / MCP:** 검색 및 데이터 수집용 MCP 서버 (딥리서치 목적)

## 4. 데이터베이스 및 스토리지 (인프라)
- **DB & Auth:** Supabase (PostgreSQL 기반 BaaS)
  - 데이터 단위: 유저, 템플릿 목록, 이력(History)
- **Storage:** Supabase Storage
  - 유저 업로드용 원본 `.pptx` 템플릿 저장, AI가 생성완료한 결과물 임시 스토리지 라우팅 저장.

## 5. 핵심 Data Flow (아키텍처 흐름)
1. **클라이언트:** 생성 폼(주제, 장수선택(8장), 템플릿/폰트 선택) 데이터를 FastAPI로 비동기 전송 POST.
2. **FastAPI (큐 삽입):** 큐에 작업을 집어넣고 프론트엔드에 `Task ID` 우선 반환.
3. **Task Worker:**
   - Gemini API 호출 -> 8장 분량의 내용 JSON 추출.
   - Storage에서 유저 템플릿 다운로드.
   - `python-pptx`로 JSON 텍스트 삽입 + 선택된 폰트명 강제 주입 + **파일 속성(메타데이터) 저장**.
4. **Task Worker:** 완성된 `.pptx` 스토리지를 업로드 후, DB의 히스토리 내역 업데이트 처리.
5. **클라이언트:** `Task ID` 상태 점검(Polling/SSE) 완료 시, 다운로드 버튼 활성화 제공.
