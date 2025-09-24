import os
import shutil
import tempfile
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# NOTE: Local 개발 용 sqlite 사용
# from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

import src.agent.workflow as wk
from src.agent.modules.states import AgentState

"""
lifespan 설정
"""
# NOTE: 로컬 개발 용 sqlite lifespan
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """
#     FastAPI lifespan Checkpointer.
#     AgentState가 매 요청마다 초기화되지 않도록 해주는 역할
#     - 서버 시작 시: DB와 연결된 Checkpointer를 생성하여 app.state에 저장
#     - 1회의 DB 연결만으로 모든 요청 처리 가능
#     """
#     async with AsyncSqliteSaver.from_conn_string("checkpoint.sqlite") as checkpointer:
#         app.state.checkpointer = checkpointer
#         print("Checkpointer Ready.")
#         yield
#     print("Checkpointer Closed.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 랩터(Raptor)나 다른 배포 환경에 설정된 환경 변수에서 DB URL을 가져옴
    DB_URL = os.environ.get("LANGGRAPH_DB_URL")
    
    if not DB_URL:
        raise RuntimeError("LANGGRAPH_DB_URL 환경 변수가 설정되지 않았습니다.")
        
    async with AsyncPostgresSaver.from_conn_string(DB_URL) as checkpointer:
        await checkpointer.setup()
        
        app.state.checkpointer = checkpointer
        print("PostgreSQL Checkpointer Ready.")
        yield
    print("PostgreSQL Checkpointer Closed.")


"""
ResponseModel 설정
"""
class PreprocessResumeResponse(BaseModel):
    # 이력서 전처리 후에는 이력서의 주요 정보만 요약해서 보내줌
    resume_details: Dict[str, Any] = Field(description="이력서에서 추출된 주요 정보")

class PreprocessJdResponse(BaseModel):
    # JD 전처리 후에는 JD의 주요 정보만 요약해서 보내줌
    jd_details: Dict[str, Any] = Field(description="JD에서 추출된 주요 정보")

class AnalyzeResumeResponse(BaseModel):
    # 이력서 분석 결과만 반환
    applicant_skills: str = Field(description="이력서 역량 분석 결과")

class AnalyzeRecruitResponse(BaseModel):
    # 이력서-JD 비교 분석 결과만 반환
    applicant_recruitment: str = Field(description="채용 공고 기반 종합 분석 결과")


app = FastAPI(lifespan=lifespan)

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


"""
endpoint 설정
"""
@app.post("/preprocess-resume")
async def preprocess_resume_endpoint(
    request: Request,
    thread_id: str = Form(...),
    resume_file: UploadFile = File(...)
):
    """이력서 파일을 받아 전처리하고, 해당 thread_id의 상태를 업데이트합니다."""
    # ... (파일 저장 및 예외 처리 로직) ...
    temp_file_path = None
    try:
        # 파일 임시 저장 로직
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            shutil.copyfileobj(resume_file.file, tmp_file)
            temp_file_path = tmp_file.name

        graph = wk.PreprocessResumeWorkflow(AgentState).build()
        work = graph.compile(checkpointer=request.app.state.checkpointer)

        initial_state = {"resume_file": temp_file_path}
        config = {"configurable": {"thread_id": thread_id}}
        
        await work.ainvoke(initial_state, config=config)
        
        final_state = await work.aget_state(config)
        return {"resume_details": final_state.values.get("resume_details", {})}

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@app.post("/preprocess-jd")
async def preprocess_jd_endpoint(
    request: Request,
    thread_id: str = Form(...),
    jd_url: str = Form(...)
):
    """JD URL을 받아 전처리하고, 해당 thread_id의 상태를 업데이트합니다."""
    graph = wk.PreprocessJDWorkflow(AgentState).build()
    work = graph.compile(checkpointer=request.app.state.checkpointer)

    initial_state = {"jd_url": jd_url}
    config = {"configurable": {"thread_id": thread_id}}

    await work.ainvoke(initial_state, config=config)
    
    final_state = await work.aget_state(config)
    return {"jd_details": final_state.values.get("jd_details", {})}


@app.post("/analyze-resume")
async def analyze_resume_endpoint(
    request: Request,
    thread_id: str = Form(...),
):
    """해당 thread_id의 이력서를 분석하고, 상태를 업데이트"""
    graph = wk.AnalyzeResumeWorkflow(AgentState).build()
    work = graph.compile(checkpointer=request.app.state.checkpointer)

    config = {"configurable": {"thread_id": thread_id}}
    current_state_snapshot = await work.aget_state(config)
    initial_state = current_state_snapshot.values

    await work.ainvoke(initial_state, config=config)
    
    final_state = await work.aget_state(config)
    return {"applicant_skills": final_state.values.get("applicant_skills", "분석 결과 없음")}


@app.post("/analyze-recruit")
async def analyze_recruit_endpoint(
    request: Request,
    thread_id: str = Form(...),
):
    """해당 thread_id의 이력서와 JD를분석하고, 상태를 업데이트"""
    graph = wk.AnalyzeRecruitWorkflow(AgentState).build()
    work = graph.compile(checkpointer=request.app.state.checkpointer)

    config = {"configurable": {"thread_id": thread_id}}
    current_state_snapshot = await work.aget_state(config)
    initial_state = current_state_snapshot.values

    await work.ainvoke(initial_state, config=config)
    
    final_state = await work.aget_state(config)
    return {"applicant_recruitment": final_state.values.get("applicant_recruitment", "분석 결과 없음")}