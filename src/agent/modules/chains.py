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
            position = lambda x: x["resume"]
        )
        | prompt
        | model
        | StrOutputParser()
    )


# JD 분해
def set_jd_chain(prompt: str, model: str = get_gemini_llm) -> RunnableSerializable:
    return (
        RunnablePassthrough.assign(
            position = lambda x: x["job_description"]
        )
        | prompt
        | model
        | StrOutputParser()
    )


# 이력서 평가
def set_resume_evaluation_chain(prompt: str, model: str = get_gemini_llm) -> RunnableSerializable:
    return (
        RunnablePassthrough.assign(
            position = lambda x: x["resume_details"]
        )
        | prompt
        | model
        | StrOutputParser()
    )