import uuid # String ID 기본값 생성을 위해 추가
from sqlalchemy import Column, String, DateTime, func, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID # UUID 타입을 위해 추가

Base = declarative_base()

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True, nullable=False)
#     email = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     is_active = Column(Boolean, default=True)

def generate_cuid():
    # Prisma의 CUID와 완전히 동일하진 않지만, 고유한 문자열 ID를 생성하는 예시
    # 실제 프로덕션에서는 CUID 라이브러리(예: python-cuid) 사용을 고려
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "User"  # Prisma 스키마와 테이블명 통일 (대소문자 주의)
    
    id = Column(String, primary_key=True, default=generate_cuid)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)  # nullable=True로 선택적 필드 설정
    passwordHash = Column(String, nullable=True) # 필드명 변경, nullable=True로 설정
    
    # Prisma의 @default(now())와 @updatedAt에 해당
    createdAt = Column(DateTime, server_default=func.now())
    updatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # is_active 필드가 Prisma 스키마에 없으므로 일단 주석 처리 또는 제거
    # is_active = Column(Boolean, default=True) 
