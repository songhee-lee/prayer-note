from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# 비동기 엔진 생성
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

# 비동기 세션 팩토리
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    # autocommit=False,  <-- 삭제 (SQLAlchemy 2.0에서 제거됨)
    # autoflush=False,   <-- 삭제 권장 (기본값 True 사용. 필요하다면 유지해도 됨)
)

# Base 클래스 생성
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    데이터베이스 세션 의존성
    async with 문을 사용하여 세션의 생성과 종료를 자동으로 관리합니다.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            # 요청 처리가 성공적으로 끝나면 여기서 커밋을 할 수도 있습니다.
            # await session.commit() 
        except Exception:
            # 에러 발생 시 변경사항 롤백
            await session.rollback()
            raise
        # finally: await session.close() <-- 삭제함
        # 이유: async with 블록을 빠져나갈 때 자동으로 close()가 호출됩니다.
        # 여기서 명시적으로 호출하면 이중으로 닫게 되어 오류가 발생할 수 있습니다.

async def init_db():
    """데이터베이스 초기화 (테이블 생성)"""
    # 모든 모델을 임포트하여 Base.metadata에 등록
    # 순환 참조 방지를 위해 함수 내부에서 import
    from app.models import User, Prayer, PrayerProgress  # noqa: F401

    async with engine.begin() as conn:
        # 변경된 메타데이터를 DB에 반영
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    """데이터베이스 연결 종료"""
    await engine.dispose()