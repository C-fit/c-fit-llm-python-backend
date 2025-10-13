from fastapi import APIRouter, Depends, UploadFile, File, Form
from src.services import oneclick_services
from src.api.dependencies import get_checkpointer

from src.core.auth import get_current_active_user
from src.models.user import User

router = APIRouter()


# 이력서 분석
@router.post("/resume")
async def oneclick_resume_endpoint(
    resume_file: UploadFile = File(...),
    checkpointer: any = Depends(get_checkpointer),
    current_user: User = Depends(get_current_active_user)
):    
    current_state = await oneclick_services.oneclick_resume(
        checkpointer=checkpointer,
        resume_file=resume_file
    )
    return {
        "applicant_skills": current_state.values.get(
            "applicant_skills", "분석 결과 없음"
        ),
        "processed_by": current_user.username
    }


# 핏 분석
@router.post("/fit")
async def oneclick_fit_endpoint(
    resume_file: UploadFile = File(...),
    jd_url: str = Form(...),
    checkpointer: any = Depends(get_checkpointer),
    current_user: User = Depends(get_current_active_user)
):    

    current_state = await oneclick_services.oneclick_fit(
        checkpointer=checkpointer,
        resume_file=resume_file,
        jd_url=jd_url
    )

    return {
        "applicant_recruitment": current_state.values.get(
            "applicant_recruitment", "분석 결과 없음"
        ),
        "processed_by": current_user.username
    }