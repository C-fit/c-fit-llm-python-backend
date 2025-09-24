import os
import shutil
import tempfile
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from typing import Optional
from contextlib import asynccontextmanager

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

import src.agent.workflow as wk
from src.agent.modules.states import AgentState

"""
lifespan 설정
"""
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan Checkpointer.
    AgentState가 매 요청마다 초기화되지 않도록 해주는 역할
    - 서버 시작 시: DB와 연결된 Checkpointer를 생성하여 app.state에 저장
    - 1회의 DB 연결만으로 모든 요청 처리 가능
    """
    async with AsyncSqliteSaver.from_conn_string("checkpoint.sqlite") as checkpointer:
        app.state.checkpointer = checkpointer
        print("Checkpointer Ready.")
        yield
    print("Checkpointer Closed.")


app = FastAPI(lifespan=lifespan)


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
        return final_state.values

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
    return final_state.values


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
    return final_state.values


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
    return final_state.values