import os
from celery_app import celery_app
from ai_engine import generate_ppt_content
from ppt_generator import generate_ppt_from_json

@celery_app.task(bind=True)
def generate_presentation_task(self, topic: str, slide_count: int, template_path: str = None, font_name: str = "맑은 고딕"):
    """
    백그라운드에서 AI 리서치 및 PPT 생성을 순차적으로 실행하는 태스크.
    FastAPI와 클라이언트가 폴링(Polling)할 수 있도록 진행률(상태)를 지속 업데이트합니다.
    """
    try:
        # 진행률 10%: 리서치 시작
        self.update_state(state='PROGRESS', meta={'message': 'AI 엔진: 리서치 및 슬라이드 구조화를 진행 중입니다...', 'progress': 10})
        
        # 1. AI 모듈 (Gemini 2.5 Flash 호출)
        ai_result = generate_ppt_content(topic, slide_count)
        
        # 진행률 50%: 리서치 완료, PPT 렌더링 준비
        self.update_state(state='PROGRESS', meta={'message': 'PPT 조립 엔진: 구조화된 자료를 바탕으로 슬라이드를 렌더링하고 있습니다...', 'progress': 50})
        
        # 임시 출력 파일명 (원래는 유니크한 ID 기반으로 S3나 Storage에 업로드해야 함)
        output_filename = f"ppt_result_{self.request.id}.pptx"
        output_filepath = os.path.join(os.getcwd(), output_filename)
        
        # 2. PPT 모듈 (python-pptx 결합)
        final_path = generate_ppt_from_json(ai_result, template_path=template_path, output_path=output_filepath, font_name=font_name)
        
        # 처리 완료 (100%)
        return {
            "status": "COMPLETED",
            "file_path": final_path,
            "message": "PPT 생성이 완벽하게 끝났습니다!"
        }
    except Exception as e:
        # 에러 발생 시 실패 상태로 기록 (에러 복구 루프의 핵심 단서)
        self.update_state(state='FAILURE', meta={'exc_type': type(e).__name__, 'exc_message': str(e), 'progress': 0})
        raise e
