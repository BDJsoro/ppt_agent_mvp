from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from celery.result import AsyncResult
from typing import Optional
import uvicorn
from tasks import generate_presentation_task
from celery_app import celery_app

app = FastAPI(
    title="PPT Agent API",
    description="FastAPI Backend for PPT Automation Agent",
    version="1.0.0"
)

# CORS 설정 (Next.js 프론트엔드 연동)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    topic: str
    slide_count: int = 8
    template_path: Optional[str] = None
    font_name: str = "맑은 고딕"

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "PPT Agent Backend is actively running."}

@app.post("/api/generate")
async def start_generation(req: GenerateRequest):
    """태스크를 Celery 큐에 밀어넣고 task_id를 즉각 반환합니다."""
    task = generate_presentation_task.delay(
        topic=req.topic,
        slide_count=req.slide_count,
        template_path=req.template_path,
        font_name=req.font_name
    )
    return {"task_id": task.id, "status": "QUEUED", "message": "성공적으로 큐 대기열에 진입했습니다."}

@app.get("/api/status/{task_id}")
async def get_task_status(task_id: str):
    """Task ID를 기반으로 대기번호 처리 및 진행률 상태(Progress)를 조회합니다."""
    task_result = AsyncResult(task_id, app=celery_app)
    
    response = {
        "task_id": task_id,
        "status": task_result.status,
    }
    
    if task_result.state == 'PENDING':
        response["progress"] = 0
        response["message"] = "대기열(Queue)에서 차례를 기다리고 있습니다..."
    elif task_result.state == 'PROGRESS':
        response["progress"] = task_result.info.get("progress", 0)
        response["message"] = task_result.info.get("message", "로딩 중...")
    elif task_result.state == 'SUCCESS':
        response["progress"] = 100
        response["result"] = task_result.result
    elif task_result.state == 'FAILURE':
        response["progress"] = 0
        response["error"] = str(task_result.info)
        
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
