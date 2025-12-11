"""세션 파일 테스트"""
import json
from pathlib import Path

SESSION_DIR = Path.home() / ".prayer_note"
SESSION_FILE = SESSION_DIR / "session.json"

print(f"세션 파일 경로: {SESSION_FILE}")
print(f"세션 파일 존재: {SESSION_FILE.exists()}")

if SESSION_FILE.exists():
    with open(SESSION_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"\n저장된 세션 데이터:")
    print(json.dumps(data, ensure_ascii=False, indent=2))
else:
    print("\n저장된 세션 파일이 없습니다.")
