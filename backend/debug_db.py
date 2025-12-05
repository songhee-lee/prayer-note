"""
데이터베이스 연결 디버깅 스크립트
"""
import asyncio
from app.core.database import AsyncSessionLocal, engine, init_db
from app.models.user import User
from app.core.security import get_password_hash
from sqlalchemy import select


async def test_db_connection():
    """데이터베이스 연결 테스트"""
    print("🔧 데이터베이스 연결 테스트 시작...\n")

    try:
        # 1. 엔진 연결 테스트
        print("1️⃣ 엔진 연결 테스트...")
        async with engine.connect() as conn:
            print("✅ 데이터베이스 엔진 연결 성공\n")

        # 2. 테이블 생성 테스트
        print("2️⃣ 테이블 초기화 테스트...")
        await init_db()
        print("✅ 테이블 초기화 성공\n")

        # 3. 세션 생성 테스트
        print("3️⃣ 세션 생성 테스트...")
        async with AsyncSessionLocal() as session:
            print("✅ 세션 생성 성공\n")

            # 4. 데이터 삽입 테스트
            print("4️⃣ 사용자 생성 테스트...")
            test_user = User(
                email="debug@test.com",
                hashed_password=get_password_hash("test123"),
                name="디버그 사용자"
            )
            session.add(test_user)
            await session.commit()
            await session.refresh(test_user)
            print(f"✅ 사용자 생성 성공: {test_user.id}\n")

            # 5. 데이터 조회 테스트
            print("5️⃣ 사용자 조회 테스트...")
            result = await session.execute(
                select(User).where(User.email == "debug@test.com")
            )
            user = result.scalar_one_or_none()
            if user:
                print(f"✅ 사용자 조회 성공:")
                print(f"   - ID: {user.id}")
                print(f"   - Email: {user.email}")
                print(f"   - Name: {user.name}")
                print(f"   - Created: {user.created_at}\n")
            else:
                print("❌ 사용자 조회 실패\n")

        print("🎉 모든 테스트 통과!")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_db_connection())
