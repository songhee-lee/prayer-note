"""
회원가입 API 테스트 스크립트
"""
import asyncio
import httpx


async def test_register():
    """회원가입 테스트"""
    base_url = "http://localhost:8000"

    # 테스트 데이터
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "테스트 사용자"
    }

    print("🧪 회원가입 API 테스트 시작...")
    print(f"요청 데이터: {user_data}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/api/v1/auth/register",
                json=user_data,
                timeout=10.0
            )

            print(f"\n📊 응답 상태 코드: {response.status_code}")
            print(f"📄 응답 내용:")
            try:
                print(response.json())
            except Exception:
                print(f"원본 텍스트: {response.text}")

            if response.status_code == 201:
                print("\n✅ 회원가입 성공!")
                return True
            else:
                print(f"\n❌ 회원가입 실패: {response.status_code}")
                return False

    except httpx.ConnectError:
        print("\n❌ 서버에 연결할 수 없습니다.")
        print("💡 FastAPI 서버가 실행 중인지 확인하세요:")
        print("   uvicorn app.main:app --reload")
        return False

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    asyncio.run(test_register())
