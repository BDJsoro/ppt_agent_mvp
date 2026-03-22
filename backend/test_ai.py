import os
from dotenv import load_dotenv
load_dotenv()

from ai_engine import generate_ppt_content

if __name__ == "__main__":
    print("Testing generate_ppt_content...")
    try:
        result = generate_ppt_content("AI in Healthcare", 3)
        print("Success!")
        import json
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")
