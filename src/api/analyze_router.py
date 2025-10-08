from fastapi import APIRouter, Depends, Form
from src.services import analyze_services
from src.api.dependencies import get_checkpointer

router = APIRouter()


# 이력서 분석
@router.post("/resume")
async def analyze_resume_endpoint(
    checkpointer: any = Depends(get_checkpointer),
    thread_id: str = Form(...),
):    
    current_state = await analyze_services.analyze_resume(
        checkpointer=checkpointer,
        thread_id=thread_id,
    )
    return {
        "applicant_skills": current_state.values.get(
            "applicant_skills", "분석 결과 없음"
        )
    }


# 핏 분석
@router.post("/fit")
async def analyze_fit_endpoint(
    checkpointer: any = Depends(get_checkpointer),
    thread_id: str = Form(...),
):    

    current_state = await analyze_services.analyze_fit(
        checkpointer=checkpointer,
        thread_id=thread_id,
    )

    return {
        "applicant_recruitment": current_state.values.get(
            "applicant_recruitment", "분석 결과 없음"
        )
    }