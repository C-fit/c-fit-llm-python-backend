import os
import httpx

from fastapi import  HTTPException, UploadFile, File, Form, Request

import src.agent.workflow as wk
from src.agent.modules.states import AgentState
from src.core.config import settings


from dotenv import load_dotenv
load_dotenv()


async def process_resume(checkpointer: any, thread_id: str, resume_file: UploadFile):
    """이력서 PDF 파일을 받아 전처리하고, 해당 thread_id의 상태를 업데이트합니다."""

    file_content = await resume_file.read()

    files = {
        'resume_file': (resume_file.filename, file_content, resume_file.content_type)
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                settings.PDF_PARSE_API_ENDPOINT,
                files=files,
                timeout=180.0
            )
            response.raise_for_status()
            result = response.json()
            
        except httpx.TimeoutException as exc:
            error_message = f"Request timed out: {exc}"
            print(error_message)
            raise HTTPException(status_code=504, detail=f"Request to the processing service timed out at {exc.request.url!r}.")
            
        except httpx.RequestError as exc:
            error_message = f"An unexpected request error occurred: {exc}"
            print(error_message)
            raise HTTPException(status_code=500, detail=f"An error occurred while requesting {exc.request.url!r}.")
        
    graph = wk.PreprocessResumeWorkflow(AgentState).build()
    work = graph.compile(checkpointer=checkpointer)

    initial_state = result
    config = {"configurable": {"thread_id": thread_id}}

    await work.ainvoke(initial_state, config=config)
    
    final_state = await work.aget_state(config)
    return final_state


async def process_jd(checkpointer: any, thread_id: str, jd_url: str):
    """JD URL을 받아 전처리하고, 해당 thread_id의 상태를 업데이트합니다."""

    graph = wk.PreprocessJDWorkflow(AgentState).build()
    work = graph.compile(checkpointer=checkpointer)

    initial_state = {"jd_url": jd_url}
    config = {"configurable": {"thread_id": thread_id}}

    await work.ainvoke(initial_state, config=config)
    
    final_state = await work.aget_state(config)
    return final_state
