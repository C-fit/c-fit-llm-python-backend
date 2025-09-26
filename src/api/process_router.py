from fastapi import APIRouter, Depends, UploadFile, File, Form
from src.services import process_services
from src.api.dependencies import get_checkpointer

router = APIRouter()


# 이력서 추출
@router.post("/resume")
async def process_resume_endpoint(
    checkpointer: any = Depends(get_checkpointer),
    thread_id: str = Form(...),
    resume_file: UploadFile = File(...)
):    
    current_state = await process_services.process_resume(
        checkpointer=checkpointer,
        thread_id=thread_id,
        resume_file=resume_file
    )
    return {
        "resume_details": current_state.values.get(
            "resume_details", {}
        )
    }


# 채용 공고 추출
@router.post("/jd")
async def process_jd_endpoint(
    checkpointer: any = Depends(get_checkpointer),
    thread_id: str = Form(...),
    jd_url: str = Form(...)
):
    current_state = await process_services.process_jd(
        checkpointer=checkpointer,
        thread_id=thread_id,
        jd_url=jd_url
    )

    return {
        "jd_details": current_state.values.get(
            "jd_details", {}
        )
    }