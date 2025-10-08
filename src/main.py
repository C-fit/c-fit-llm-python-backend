from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.db import lifespan_manager
from src.api import process_router, analyze_router, oneclick_router

# FastAPI 애플리케이션 생성 및 lifespan 등록
app = FastAPI(
    title="AI Resume Service API",
    description="이력서 처리, 분석, JD와의 적합도 분석 기능을 제공하는 API입니다.",
    version="0.2.0",
    lifespan=lifespan_manager
)

origins = [
    "http://localhost:3000",  # 로컬 FE 개발 서버
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # 허용할 출처 목록
    allow_credentials=True,       # 쿠키를 포함한 요청 허용 여부
    allow_methods=["*"],          # 허용할 HTTP 메서드 (GET, POST 등)
    allow_headers=["*"],          # 허용할 HTTP 헤더
)

app.include_router(oneclick_router.router, prefix="/oneclick", tags=["One Click Analysis"])
app.include_router(process_router.router, prefix="/process", tags=["Data Processing"])
app.include_router(analyze_router.router, prefix="/analyze", tags=["AI Analysis"])


@app.get("/", tags=["Root"])
async def root():
    """API 서버가 정상적으로 실행 중인지 확인합니다."""
    return {"message": "Welcome to AI Resume Service API!"}
