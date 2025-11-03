"""Langchain 모듈
각 Agent 노드에서 사용하는 프롬프트와 모델을 Langchain 문법으로 정의, 결합합니다.
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
            resume_txt = lambda x: x["resume_txt"]
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


# Fit 평가
def set_fit_evaluation_chain(prompt: str, model: str = get_gemini_llm) -> RunnableSerializable:
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


# Fit 종합 평가
def set_total_evaluation_chain(prompt: str, model: str = get_gemini_llm) -> RunnableSerializable:
    return (
        RunnablePassthrough.assign(
            standard_analysis = lambda x: x["standard_analysis"],
            deep_dives_analysis = lambda x: x["deep_dives_analysis"]
        )
        | prompt
        | model
        | StrOutputParser()
    )