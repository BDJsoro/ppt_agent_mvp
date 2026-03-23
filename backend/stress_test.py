import requests
import time

API_URL = "http://localhost:8000"

def test_async_queue():
    print("🚀 [Stress Test] 동시 생성 3건 일괄 전송 시작...")
    topics = ["미래 자동차 기술", "가상화폐 전망", "인공지능의 윤리"]
    task_ids = []
    
    # 1. 3개 동시에 쏘아서 큐에 넣기
    for topic in topics:
        res = requests.post(f"{API_URL}/api/generate", json={"topic": topic, "slide_count": 3})
        if res.status_code == 200:
            task_id = res.json().get('task_id')
            task_ids.append(task_id)
            print(f"[API] '{topic}' 요청 접수 완료 -> Task ID: {task_id}")
        else:
            print(f"[오류] {topic} 요청 실패: {res.text}")

    # 2. Polling 으로 백그라운드 서버 상태 조회
    print("\n⏳ [Polling] 결과 추적 진행...")
    completed = 0
    while completed < len(task_ids):
        time.sleep(3)
        print("-" * 50)
        completed = 0
        for task_id in task_ids:
            res = requests.get(f"{API_URL}/api/status/{task_id}")
            data = res.json()
            status = data.get("status")
            progress = data.get("progress", 0)
            msg = data.get("message", "")
            
            if status == "SUCCESS":
                completed += 1
                result_path = data.get("result", {}).get("file_path", "N/A")
                print(f"[{task_id[-6:]}] ✅ 완료! 파일 경로: {result_path}")
            elif status == "FAILURE":
                completed += 1
                print(f"[{task_id[-6:]}] ❌ 실패! 에러: {data.get('error')}")
            else:
                print(f"[{task_id[-6:]}] 🔄 {status} ({progress}%) - {msg}")

if __name__ == "__main__":
    test_async_queue()
