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
    이력서는 <Resume>를 참고하고, 최종 심사 결과는 <Style>의 양식에 맞게 보고서로 작성하라.

    # Resume
    {resume_details}

    # Style
    ## 평가 기준
    아래 다섯 가지 평가 기준에 부합하도록 지원자의 이력서를 평가하라.
    **기술 역량 (Technical Competence)**
    - 비즈니스 요구사항을 이해하고, 이에 맞는 적절한 기술 스택과 아키텍처를 설계하여 기능을 구현한 경험
    - 확장성과 안정성을 고려한 시스템 아키텍처 설계 및 구축 경험
    - 클린 코드, 테스트 코드 작성 등 코드 품질 및 유지보수성에 대한 이해와 이를 실제 프로젝트에 적용한 사례
    - 설계부터 개발, 테스트, 배포, 운영까지 제품의 End-to-End 생명 주기를 경험하고 개선해 본 이력

    **문제 해결 및 실행력 (Problem-Solving & Execution)**
    - 문제의 현상 너머에 있는 핵심 원인을 파악하고, 이를 측정 가능한 구체적인 지표(Metric)로 정의하는 능력
    - 정의된 문제를 해결하기 위해 논리적인 가설을 세우고, 작은 단위로 빠르게 실행하며 검증하는 사이클을 반복한 경험
    - 기술적 난제나 복잡한 버그를 해결하여 비즈니스 또는 프로덕트 성과(예: 성능 개선, 비용 절감, 사용자 경험 향상)에 실질적으로 기여한 사례

    **학습 및 성장 잠재력 (Learning & Growth Potential)**
    - 새로운 기술, 언어, 도메인에 대한 빠른 학습 능력과 이를 실제 프로젝트에 성공적으로 적용한 사례
    - 기술 블로그 운영, 오픈소스 기여, 개인 프로젝트 진행, 세미나 발표 등 자기주도적 학습에 대한 꾸준한 노력과 결과물
    - 경험한 실패를 회고하고 원인을 분석하여, 배운 점을 다음 프로젝트나 업무 방식에 적용하여 개선한 이력

    **오너십 (Ownership)**
    - 주어진 과업을 완수하는 것을 넘어, 스스로 문제를 발견하고 개선 방안을 적극적으로 제안하여 프로젝트를 주도한 경험
    - 담당한 기능의 품질과 마일스톤에 대해 높은 책임감을 보이며, 예상치 못한 이슈 발생 시 해결을 위해 끝까지 노력한 사례
    - 프로젝트의 성공을 자신의 일처럼 여기고, 팀의 목표 달성을 위해 필요하다면 명시된 역할 이상의 기여를 하려는 태도

    **협업 및 소통 (Collaboration & Communication)**
    - 기획, 디자인 등 다른 직군과 원활하게 소통하며 복잡한 요구사항을 조율하고 성공적으로 제품을 만들어낸 경험
    - 기술적인 논의 과정에서 명확한 근거를 바탕으로 자신의 의견을 제시하고, 동시에 다른 팀원의 의견을 경청하여 더 나은 결론을 도출하는 능력
    - 동료의 성장을 돕기 위해 코드 리뷰에 적극적으로 참여하거나, 팀 내에 지식을 공유하고 기술 문서를 작성한 이력
    """

    return PromptTemplate(
        template=template,
        input_variables=["resume_details"]
    )