"""LangChain 체인을 설정하는 함수 모듈

LCEL(LangChain Expression Language)을 사용하여 체인을 구성합니다.
기본적으로 modules.prompt 템플릿과 modules.models 모듈을 사용하여 LangChain 체인을 생성합니다.
"""
from typing import List
from langchain.schema.runnable import RunnablePassthrough, RunnableSerializable
from langchain_core.output_parsers import StrOutputParser
from src.agent.modules.models import get_gemini_llm
from src.agent.modules.states import ProjectAndAchievementsDict, ExperiencesDict


# Resume 분해
def set_decomposition_chain(prompt: str, model: str = get_gemini_llm) -> RunnableSerializable:
    return (
        RunnablePassthrough.assign(
            resume = lambda x: x["resume"]
        )
        | prompt
        | model
        | StrOutputParser()
    )


# JD 분해
def set_jd_chain(prompt: str, model: str = get_gemini_llm) -> RunnableSerializable:
    return (
        RunnablePassthrough.assign(
            job_description = lambda x: x["job_description"]
        )
        | prompt
        | model
        | StrOutputParser()
    )


# 이력서 평가
def set_resume_evaluation_chain(prompt: str, model: str = get_gemini_llm) -> RunnableSerializable:
    return (
        RunnablePassthrough.assign(
            resume_details = lambda x: x["resume_details"]
        )
        | prompt
        | model
        | StrOutputParser()
    )


# Resume/JD 비교 심사
def set_recruit_evaluation_chain(prompt: str, model: str = get_gemini_llm) -> RunnableSerializable:
    return (
        RunnablePassthrough.assign(
            company = lambda x: x["company"],
            company_inforamtion = lambda x: x["company_information"],
            title = lambda x: x["title"],
            introduction = lambda x: x["introduction"],
            responsibilities = lambda x: x["responsibilities"],
            qualifications = lambda x: x["qualification"],
            preference = lambda x: x["preference"],
            skills = lambda x: x["skills"],
            tech_stacks = lambda x: x["tech_stacks"],
            resume_details = lambda x: x["resume_details"]
        )
        | prompt
        | model
        | StrOutputParser()
    )