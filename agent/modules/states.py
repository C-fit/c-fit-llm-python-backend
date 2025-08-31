"""
이미지 Workflow의 상태를 정의하는 모듈

이 모듈은 이미지 기반 콘텐츠 생성을 위한 Workflow에서 사용되는 상태 정보를 정의합니다.
LangGraph의 상태 관리를 위한 클래스를 포함합니다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, TypedDict, Dict, Union

from langgraph.graph.message import add_messages

from typing import TypedDict, Dict, List, Any, Optional

"""
각 노드에서 사용하는 딕셔너리 자료형
"""
class ExperiencesDict(TypedDict):
    # 재직 회사
    company: str
    # 근속 년수
    years: int
    # 담당 직무
    role: str
    # 진행한 업무
    projects: str
    # 성과
    achievements: str


class ProjectsDict(TypedDict):
    # 프로젝트 명
    title: str
    # 개인/협업 여부
    people: bool
    # 담당 업무
    role: str
    # 성과
    achievements: str


class ResumeDict(TypedDict):
    # 직무 유형
    position: str
    # 기술 스택
    tech_stacks: str
    # 경력 년차
    years: int
    # 수상 내역
    awards: str
    # 자격증
    certifications: str
    # 특이사항
    etcetra: str


class JobDescriptionDict(TypedDict):
    # 직무명
    title: str
    # 직무 요약
    introduction: str
    # 주요 업무
    responsibilities: str
    # 자격요건
    qualification: str
    # 우대사항
    preference: str
    # 필요 역량
    skills: str
    # 혜택 및 복지
    benefits: str
    # 근무 조건
    conditions: str
    # 채용 프로세스
    process: str
    # 기술 스택
    tech_stacks: str


"""
Agent State
"""
class AgentState(TypedDict):
    # 이력서 & JD 원본
    resume: str
    job_description: str

    # 분해된 이력서 & JD
    resume_details: ResumeDict
    jd_details: JobDescriptionDict