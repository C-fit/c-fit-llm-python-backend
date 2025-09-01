"""프롬프트 템플릿을 생성하는 함수 모듈

프롬프트 템플릿을 생성하는 함수 모듈을 구성합니다.
기본적으로 PromptTemplate을 사용하여 프롬프트 템플릿을 생성하고 반환합니다.
"""

from langchain.prompts import PromptTemplate

def get_resume_prompt() -> str :
    """이력서를 토대로 직무 카테고리 등 키워드를 추출하는 프롬프트

    Args:
        resume (str): 이력서 전체 string
    
    Returns:
        이력서 추출 프롬프트 (PromptTemplate)
    """
    template = """# Role
    너는 이력서를 토대로 지원자의 직무 유형, 기술 스택, 경력, 특이사항을 추출하는 채용 도우미다.
    이력서는 <Resume>를 참고하고, 추출한 키워드는 <Style>의 양식에 맞게 작성하라.

    # Resume
    {resume}

    # Style
    - position: 직무 유형(AI 엔지니어, ML 엔지니어, DevOps 엔지니어, ML 리서처, Backend 엔지니어 등)
    - tech_stacks: 기술 스택(사용하는 언어와 프레임워크, 라이브러리 등; Python, Go, React, Node.js, Kubernetes, Docker, Langchain 등)
    - years: 지원자의 경력 년차(무경력일 경우 '신입', 경력직일 경우 'n년차')
    - awards: 수상 내역
    - certifications: 자격증
    - etcetra: 특이사항(병역특례, 보훈유공자 등)

    Output must be a valid JSON object only. Do NOT include ``` or any Markdown formatting.
    """

    return PromptTemplate(
        template=template,
        input_variables=["resume"]
    )


def get_experiences_prompt() -> str:
    """이력서를 토대로 직무 카테고리 등 키워드를 추출하는 프롬프트
    
    Args:
        resume (str): 이력서 전체 string
    
    Returns:
        이력서 경력 프롬프트 (PromptTemplate)
    """
    template = """# Role
    너는 이력서의 경력 사항을 추출하는 채용 도우미다.
    이력서는 <Resume>를 참고하고, 추출한 경력은 <Style>을 참고하여 <Few-shot Example>의 양식에 맞게 작성하라.

    # Resume
    {resume}

    # Style
    - company: 재직한 회사명
    - years: 해당 회사의 근속 년수. 기재되지 않았을 시 'None'
    - role: 해당 직장에서 담당한 직무명
    - project: 해당 직장에서 진행한 프로젝트
    - achievements: 해당 프로젝트에서 달성한 성과들

    # Few-shot Example
    {
        "company": "테크 컴퍼니",
        "years": 3,
        "role": "백엔드 개발자",
        "projects": [
            {
                "project": "사용자 인증 시스템 개발",
                "achievements": [
                    "로그인 성공률 15% 향상",
                    "보안 취약점 3건 해결",
                    "사용자 만족도 90% 달성"
                ]
            },
            {
                "project": "API 성능 최적화",
                "achievements": [
                    "응답 시간 50% 단축",
                    "서버 리소스 사용량 30% 절약"
                ]
            },
            {
                "project": "데이터베이스 마이그레이션",
                "achievements": [
                    "다운타임 없이 성공적으로 완료"
                ]
            }
        ]
    }

    Output must be a valid JSON object only. Do NOT include ``` or any Markdown formatting.
    """

    return PromptTemplate(
        template=template,
        input_variables=["resume"]
    )


def get_jd_prompt() -> str :
    """
    이력서를 토대로 직무 카테고리 등 키워드를 추출하는 프롬프트

    Args
        - 이력서
    """

    template = """# Role
    너는 채용공고의 직무명, 자격요건, 우대사항 등을 추출하는 채용 도우미다.
    이력서는 <Resume>를 참고하고, 최종 결과는 <Style>의 양식에 맞게 작성하라.

    # Job Description
    {job_description}

    # Style
    - title: 직무명(예: 백엔드 엔지니어, 데이터 사이언티스트 등)
    - introduction: 직무 요약
    - responsibilities: 주요 업무
    - qualification: 자격요건
    - preference: 우대사항
    - skills: 필요 역량
    - benefits: 혜택 및 복지
    - conditions: 근무 조건
    - process: 채용 프로세스(전형 절차, 지원 방법 및 일정 등)
    - tech_stacks: 기술 스택(주요 개발 도구, 라이브러리, 언어 등)

    모든 요소는 요약/수정/편집 없이 Job Description의 원본 내용을 그대로 작성하라.
    Output must be a valid JSON object only. Do NOT include ``` or any Markdown formatting.
    """

    return PromptTemplate(
        template=template,
        input_variables=["job_description"]
    )


def get_analysis_prompt() -> str :
    """
    이력서와 JD를 비교 분석하는 프롬프트

    Args
        - 이력서
        - JD
    """

    template = """# Role
    너는 이력서와 Job Description을 비교 분석하여, 지원자의 역량과 경험을 토대로 해당 JD와 지원자의 적합성을 심사하는 인사 담당자이다.
    이력서는 <Resume>, JD는 <Job Description>을 참고하고, 최종 심사 결과는 <Style>의 양식에 맞게 작성하라.

    # Resume
    {resume_details}

    # Job Description
    {jd_details}

    # Style
    - strength: JD의 


    Output must be a valid JSON object only. Do NOT include ``` or any Markdown formatting.
    """

    return PromptTemplate(
        template=template,
        input_variables=["resume_details", "jd_details"]
    )