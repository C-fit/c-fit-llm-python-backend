from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# 기본 공유 필드
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None

# 회원가입 시 요청 데이터
class UserCreate(UserBase):
    password: str
    
# DB 저장을 위한 내부 모델 (passwordHash 포함)
class UserInDB(UserBase):
    passwordHash: str
    
    class Config:
        from_attributes = True

# API 응답 데이터 (비밀번호 제외)
class UserOut(UserBase):
    id: str
    # createdAt, updatedAt 필드도 필요하다면 추가
    
    class Config:
        from_attributes = True

# 토큰 관련 스키마는 거의 동일하나, sub 필드가 email 또는 id가 될 수 있음
class TokenData(BaseModel):
    # JWT의 subject를 email로 사용할 경우
    email: Optional[str] = None
