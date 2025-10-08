from fastapi import APIRouter, Depends, UploadFile, File, Form
from src.services import oneclick_services
from src.api.dependencies import get_checkpointer

router = APIRouter()


# 이력서 분석
@router.post("/resume")
async def oneclick_resume_endpoint(
    checkpointer: any = Depends(get_checkpointer),
    thread_id: str = Form(...),
    resume_file: UploadFile = File(...)
):    
    current_state = await oneclick_services.oneclick_resume(
        checkpointer=checkpointer,
        thread_id=thread_id,
        resume_file=resume_file
    )
    return {
        "applicant_skills": current_state.values.get(
            "applicant_skills", "분석 결과 없음"
        )
    }


# 핏 분석
@router.post("/fit")
async def oneclick_fit_endpoint(
    checkpointer: any = Depends(get_checkpointer),
    thread_id: str = Form(...),
    resume_file: UploadFile = File(...),
    jd_url: str = Form(...)
):    

    current_state = await oneclick_services.oneclick_fit(
        checkpointer=checkpointer,
        thread_id=thread_id,
        resume_file=resume_file,
        jd_url=jd_url
    )

    return {
        "applicant_recruitment": current_state.values.get(
            "applicant_recruitment", "분석 결과 없음"
        )
    }