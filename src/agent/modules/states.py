"""Agent State 모듈
Agent가 사용하는 각 데이터들의 스키마를 정의합니다.
"""

from __future__ import annotations
from typing import Annotated, TypedDict, List, NotRequired


def merge_dict(existing: dict, new: dict) -> dict:
    """states.py의 기존값 유지를 위한 리듀서"""
    if existing is None:
        return new
    return {**existing, **new}


"""
각 노드에서 사용하는 딕셔너리 자료형
"""
class ProjectAndAchievementsDict(TypedDict):
    """프로젝트 별 성과"""
    title: str                  # 프로젝트명
    achievements: List[str]     # 성과
    period: int                 # 개발 기간
    role: str                   # 담당 업무
    team: bool                  # 협업 여부
    company: str                # 진행한 회사

class ExperiencesDict(TypedDict):
    company: str            # 재직 회사
    period: int              # 근속 년수
    role: str               # 담당 직무
    projects: List[ProjectAndAchievementsDict]    #진행한 업무    


"""
Resume && JD schema
"""
class ResumeDict(TypedDict):
    position: str                   # 직무 유형
    tech_stacks: str                # 기술 스택
    years: int                      # 경력 년차
    awards: str                     # 수상 내역
    certifications: str             # 자격증
    publications: str               # 논문 및 출판물
    etcetra: str                    # 특이사항
    experiences: List[ExperiencesDict]    # 경력
    projects: List[ProjectAndAchievementsDict]   # 프로젝트


class JobDescriptionDict(TypedDict):
    title: str                  # 직무명
    company: str                # 회사명
    company_information: NotRequired[str]    # 회사 소개 요약
    introduction: NotRequired[str]           # 직무 요약
    responsibilities: NotRequired[str]       # 주요 업무
    qualification: NotRequired[str]          # 자격요건
    preference: NotRequired[str]             # 우대사항
    skills: NotRequired[str]                 # 필요 역량
    benefits: NotRequired[str]               # 혜택 및 복지
    conditions: NotRequired[str]             # 근무 조건
    process: NotRequired[str]                # 채용 프로세스
    tech_stacks: NotRequired[str]            # 기술 스택


"""
Agent State
"""
class APIInfo(TypedDict):
    version: str = "fit.v1.1"
    locale: str = "ko-KR"

class RequestMeta(TypedDict):
    thread_id: str
    model: str = "cf-oneclick"
    generatedAt: str

class ResumeMeta(TypedDict):
    filename: str           # 이력서 파일 이름
    pages: int              # 이력서 페이지 수

class JobMeta(TypedDict):
    title: str
    company: str

class AgentState(TypedDict):
    # 이력서 파일 & JD URL
    resume_file: str
    jd_url: str

    # 이력서 & JD 원본 text
    resume_txt: str
    job_description: str

    # 분해된 이력서 & JD
    resume_details: Annotated[ResumeDict, merge_dict]
    jd_details: JobDescriptionDict

    # 지원자 평가 관련 항목
    applicant_skills: str
    applicant_recruitment: str


    # 출력 필드
    version: str = "fit.v1.1"
    locale: str = "ko-KR"
    job_family: str
    meta: RequestMeta

    # Job 메타
    job: JobMeta

    # 이력서 메타
    resume: ResumeMeta

    # 평가 내역
    standard_analysis: str
    deep_dives_analysis: str
    overall_analysis: str