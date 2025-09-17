"""프롬프트 템플릿을 생성하는 함수 모듈

프롬프트 템플릿을 생성하는 함수 모듈을 구성합니다.
기본적으로 PromptTemplate을 사용하여 프롬프트 템플릿을 생성하고 반환합니다.
"""

from langchain.prompts import PromptTemplate


"""
Step 1. 이력서 관련 프롬프트
"""
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
    - years: 지원자의 경력 년차(무경력일 경우 '신입', 경력직일 경우 'n년차'. 인턴은 경력으로 분류하지 않는다.)
    - awards: 수상 내역
    - certifications: 자격증
    - etcetra: 특이사항(병역특례, 보훈유공자 등)

    Output must be a valid JSON object only. Do NOT include ``` or any Markdown formatting.
    """

    return PromptTemplate(
        template=template,
        input_variables=["resume"]
    )


def get_projects_prompt() -> str:
    """이력서에 기재된 프로젝트 내역을 추출하는 프롬프트
    
    Args:
        resume (str): 이력서 전체 string
    
    Returns:
        이력서 프로젝트 프롬프트 (PromptTemplate)
    """
    template = """# Role
    너는 이력서의 프로젝트 내역을 추출하는 채용 도우미다.
    이력서는 <Resume>를 참고하고, <Style>의 지침대로 추출하라.
    이 때, 사이드 프로젝트 뿐만 아니라 회사에서 진행한 프로젝트까지 모두 추출하라.

    # Resume
    {resume}

    # Style
    - title(str): 진행한 프로젝트 이름
    - achievements(List[str]): 해당 프로젝트에서 달성한 성과들
    - period(int): 해당 프로젝트의 개발 기간. 단위는 month. 기재되지 않았을 시 'None'
    - role(str): 해당 프로젝트에서 담당한 직무명
    - team(bool): 협업 여부 (1인 개발한 프로젝트이면 False)
    - company(Optional[str]): 프로젝트를 진행한 회사의 이름(이름만 추출할 것. 없을 경우 None)

    Output must be a valid JSON object only. Do NOT include ``` or any Markdown formatting.
    """

    return PromptTemplate(
        template=template,
        input_variables=["resume"]
    )


def get_experiences_prompt() -> str:
    """이력서를 토대로 경력사항을 추출하는 프롬프트
    
    Args:
        resume (str): 이력서 전체 string
    
    Returns:
        이력서 경력 프롬프트 (PromptTemplate)
    """
    template = """# Role
    너는 이력서의 경력 사항을 추출하는 채용 도우미다.
    이력서는 <Resume>를 참고하고, <Style>의 지침대로 추출하라.

    # Resume
    {resume}

    # Style
    - company(str): 재직한 회사의 이름(이름만 추출할 것)
    - period(int): 해당 회사의 근속 년수. 단위는 year. 기재되지 않았을 시 'None'
    - role(str): 해당 직장에서 담당한 직무명

    Output must be a valid JSON object only. Do NOT include ``` or any Markdown formatting.
    """

    return PromptTemplate(
        template=template,
        input_variables=["resume"]
    )


"""
Step 2. JD 관련 프롬프트
"""
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