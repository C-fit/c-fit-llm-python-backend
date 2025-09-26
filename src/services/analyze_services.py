import os
import shutil
import tempfile
import httpx
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from psycopg_pool import AsyncConnectionPool

# NOTE: Local 개발 용 sqlite 사용
# from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

import src.agent.workflow as wk
from src.agent.modules.states import AgentState

from dotenv import load_dotenv
load_dotenv()


async def analyze_resume(checkpointer: any, thread_id: str):
    """해당 thread_id의 이력서를 분석하고, 상태를 업데이트"""

    graph = wk.AnalyzeResumeWorkflow(AgentState).build()
    work = graph.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": thread_id}}
    current_state_snapshot = await work.aget_state(config)
    initial_state = current_state_snapshot.values

    await work.ainvoke(initial_state, config=config)
    
    final_state = await work.aget_state(config)
    return final_state


async def analyze_fit(checkpointer: any, thread_id: str):
    """해당 thread_id의 이력서와 JD를 분석하고, 상태를 업데이트"""

    graph = wk.AnalyzeFitWorkflow(AgentState).build()
    work = graph.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": thread_id}}
    current_state_snapshot = await work.aget_state(config)
    initial_state = current_state_snapshot.values

    await work.ainvoke(initial_state, config=config)
    
    final_state = await work.aget_state(config)
    return final_state