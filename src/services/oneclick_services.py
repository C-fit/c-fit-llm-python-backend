from fastapi import UploadFile, HTTPException
import httpx

import src.agent.workflow as wk
from src.agent.modules.states import AgentState
from src.core.config import settings


async def oneclick_resume(checkpointer: any, thread_id: str, resume_file: UploadFile):
    """해당 thread_id의 이력서를 분석하고, 상태를 업데이트"""
    file_content = await resume_file.read()

    files = {
        'resume_file': (resume_file.filename, file_content, resume_file.content_type)
    }

    headers = {
        "X-API-KEY": settings.PARSE_API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                settings.PDF_PARSE_API_ENDPOINT,
                files=files,
                headers=headers,
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
        
    graph = wk.OneclickResumeWorkflow(AgentState).build()
    work = graph.compile(checkpointer=checkpointer)

    initial_state = result
    config = {"configurable": {"thread_id": thread_id}}

    await work.ainvoke(initial_state, config=config)
    
    final_state = await work.aget_state(config)
    return final_state


async def oneclick_fit(checkpointer: any, thread_id: str, resume_file: UploadFile, jd_url: str):
    """해당 thread_id의 이력서와 JD를 분석하고, 상태를 업데이트"""

    file_content = await resume_file.read()

    files = {
        'resume_file': (resume_file.filename, file_content, resume_file.content_type)
    }

    headers = {
        "X-API-KEY": settings.PARSE_API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                settings.PDF_PARSE_API_ENDPOINT,
                files=files,
                headers=headers,
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
        
    graph = wk.OneclickFitWorkflow(AgentState).build()
    work = graph.compile(checkpointer=checkpointer)

    initial_state = {**result, "jd_url": jd_url}
    config = {"configurable": {"thread_id": thread_id}}

    await work.ainvoke(initial_state, config=config)
    
    final_state = await work.aget_state(config)
    return final_state