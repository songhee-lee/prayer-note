from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


# 사용자 등록
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    name: str = Field(..., min_length=1, max_length=100)


# 사용자 로그인
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# 사용자 응답
class UserResponse(BaseModel):
    id: UUID
    email: str
    name: str
    created_at: datetime
    
    model_config = {"from_attributes": True}


# 토큰
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# 토큰 페이로드
class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None
    type: Optional[str] = None


# 사용자 + 토큰
class UserWithToken(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
