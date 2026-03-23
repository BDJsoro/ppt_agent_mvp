import json
from ppt_generator import generate_ppt_from_json

mock_json = {
  "topic": "AI 헬스케어의 미래와 전망",
  "slides": [
    {
      "title": "도전과 전망",
      "content": [
        "의료진과 AI의 협력이 미래 헬스케어의 핵심이 됨.",
        "인공지능(AI)이 의료 분야에 혁신을 가져옴."
      ]
    },
    {
      "title": "적용 현황",
      "content": [
        "신약 개발 속도를 획기적으로 단축함.",
        "의료 영상 판독의 정확도와 속도를 높임."
      ]
    }
  ]
}

if __name__ == "__main__":
    out_path = "test_output.pptx"
    print("Testing PPT generation...")
    try:
        result_path = generate_ppt_from_json(mock_json, output_path=out_path, font_name="맑은 고딕")
        print(f"Success! Saved to {result_path}")
        
        # Verify metadata
        from pptx import Presentation
        prs = Presentation(result_path)
        print(f"Author: {prs.core_properties.author}")
        print(f"Hidden Comments Metadata: {prs.core_properties.comments}")
    except Exception as e:
        print(f"Error: {e}")
