"""
데이터베이스 초기화 스크립트
"""
import asyncio
from app.core.database import init_db, engine
from app.models import User, Prayer, PrayerProgress


async def main():
    """데이터베이스 테이블 생성"""
    print("데이터베이스 초기화 중...")

    try:
        await init_db()
        print("✅ 데이터베이스 테이블이 성공적으로 생성되었습니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
