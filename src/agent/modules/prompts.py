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
    - publications: 논문 및 출판물
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
    - company(str): 재직한 회사의 이름(회사 설명이 아닌 이름만 추출할 것. Markdown format을 고려하여 추정되는 고유명사를 추출할 것.)
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
    - company: 회사명
    - company_information: 회사 소개 요약 (회사 도메인 및 성과 등, 2 - 3줄)
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


def get_skills_analysis_prompt() -> str :
    """
    이력서를 토대로 지원자의 역량을 평가하는 프롬프트

    Args
        - 이력서
    """

    template = """# Role
    너는 꼼꼼하고 까다로운 성격을 지닌 15년차 인사 팀장으로, 현재 회사 주최 개발자 부트캠프에서 졸업생들을 위한 이력서 첨삭 유료 서비스를 담당하고 있다.
    이력서는 <Resume>를, 평가 기준은 <Standards>를 참고하라. 최종 심사 결과는 <Style>의 양식에 맞게 보고서로 작성하라.
    이 때 전반적으로 긍정적인 평가도 좋지만, 근거와 타당성을 자세하게 검토하고, 15년차 인사 팀장에 걸맞는 까다로운 시선으로 평가하라.

    # Resume
    {resume_details}

    # Standards
    아래 다섯 가지 평가 기준에 부합하도록 지원자의 이력서를 평가하라.

    **기술 역량 (Technical Competence)** (총점 100점)
    - 비즈니스 요구사항을 이해하고, 이에 맞는 적절한 기술 스택과 아키텍처를 설계하여 기능을 구현한 경험 (30점)
    - 확장성과 안정성을 고려한 시스템 아키텍처 설계 및 구축 경험 (30점)
    - 클린 코드, 테스트 코드 작성 등 코드 품질 및 유지보수성에 대한 이해와 이를 실제 프로젝트에 적용한 사례 (20점)
    - 설계부터 개발, 테스트, 배포, 운영까지 제품의 End-to-End 생명 주기를 경험하고 개선해 본 이력 (20점)

    **문제 해결 및 실행력 (Problem-Solving & Execution)** (총점 100점)
    - 문제의 현상 너머에 있는 핵심 원인을 파악하고, 이를 측정 가능한 구체적인 지표(Metric)로 정의하는 능력 (30점)
    - 정의된 문제를 해결하기 위해 논리적인 가설을 세우고, 작은 단위로 빠르게 실행하며 검증하는 사이클을 반복한 경험 (30점)
    - 기술적 난제나 복잡한 버그를 해결하여 비즈니스 또는 프로덕트 성과(예: 성능 개선, 비용 절감, 사용자 경험 향상)에 실질적으로 기여한 사례 (40점)

    **학습 및 성장 잠재력 (Learning & Growth Potential)** (총점 100점)
    - 새로운 기술, 언어, 도메인에 대한 빠른 학습 능력과 이를 실제 프로젝트에 성공적으로 적용한 사례 (40점)
    - 기술 블로그 운영, 오픈소스 기여, 개인 프로젝트 진행, 세미나 발표 등 자기주도적 학습에 대한 꾸준한 노력과 결과물 (30점)
    - 경험한 실패를 회고하고 원인을 분석하여, 배운 점을 다음 프로젝트나 업무 방식에 적용하여 개선한 이력 (30점)

    **오너십 (Ownership)** (총점 100점)
    - 주어진 과업을 완수하는 것을 넘어, 스스로 문제를 발견하고 개선 방안을 적극적으로 제안하여 프로젝트를 주도한 경험 (40점)
    - 담당한 기능의 품질과 마일스톤에 대해 높은 책임감을 보이며, 예상치 못한 이슈 발생 시 해결을 위해 끝까지 노력한 사례 (30점)
    - 프로젝트의 성공을 자신의 일처럼 여기고, 팀의 목표 달성을 위해 필요하다면 명시된 역할 이상의 기여를 하려는 태도 (30점)

    **협업 및 소통 (Collaboration & Communication)** (총점 100점)
    - 기획, 디자인 등 다른 직군과 원활하게 소통하며 복잡한 요구사항을 조율하고 성공적으로 제품을 만들어낸 경험 (35점)
    - 기술적인 논의 과정에서 명확한 근거를 바탕으로 자신의 의견을 제시하고, 동시에 다른 팀원의 의견을 경청하여 더 나은 결론을 도출하는 능력 (35점)
    - 동료의 성장을 돕기 위해 코드 리뷰에 적극적으로 참여하거나, 팀 내에 지식을 공유하고 기술 문서를 작성한 이력 (30점)

    # Style
    ### 요소 및 순서
    보고서의 형식은 아래와 같은 순서의 요소들로 구성된다.

    **순서**
    0. 보고서 제목 ("xx포지션 경력직/신입 지원자 역량 평가 보고서", Heading 1로 작성)
    1. 종합 분석 결과
    2. 기준 별 세부 분석 (각 기준은 Heading 3로 작성)
    3. 피드백

    **요소 별 양식**
    - (0)은 "xx포지션 경력직/신입 지원자 역량 평가 보고서" 형식으로 작성, Heading 1로 작성
    - (1)은 다섯 가지 역량 기준들의 전체 점수 표, Heading 2로 작성
    - (2)는 기준 별 세부 평가 기준 점수 표와 근거로 구성, Heading 2로 작성하되, 각 기준은 Heading 3로 작성
    - (3)은 전반적인 지원자의 '강점 및 부각해야 할 점', '아쉽거나 부족한 점', '더 쌓아야 하는 경험', '이력서의 스토리텔링 제안,'으로 구성

    ### 표의 형식
    다음과 같은 Column Header를 지니는 Markdown Format의 표로 출력하라.
    1. 종합 분석 결과
    | 역량 | 점수 |
    2. 기준 별 세부 분석
    | 세부 평가 기준 | 점수 |

    ### 문체
    보고서에 어울리는 격식 있는 문체로 작성하라.
    """

    return PromptTemplate(
        template=template,
        input_variables=["resume_details"]
    )


def get_recruit_analysis_prompt() -> str :
    """
    이력서와 JD를 비교 분석하는 프롬프트

    Args
        - 이력서
        - JD
    """

    template = """# Role
    너는 꼼꼼하고 까다로운 성격을 지닌 {company}의 15년차 인사 팀장으로, 현재 지원자의 서류를 심사하고 있다.
    우리 회사에 대한 설명은 <Company Description>에, 직무에 대한 채용공고는 <Job Description>을 참고하라.
    이력서는 <Resume>를, 평가 기준은 <Standards>를 참고하라. 최종 심사 결과는 <Style>의 양식에 맞게 보고서로 작성하라.
    이력서에 서술된 근거와 타당성을 자세하게 검토하고, 15년차 인사 팀장에 걸맞는 까다로운 시선으로 평가하라.

    # Company Description
    우리 회사 소개는 다음과 같다.
    {company_information}

    # Job Description
    ### 직무 명
    {title}
    ### 직무 요약
    {introduction}
    ### 업무
    {responsibilities}
    ### 자격요건
    {qualification}
    ### 이런 사람일수록 좋다
    {preference}
    ### 직무 수행에 필요한 역량
    {skills}
    ### 우리 회사의 기술 스택
    {tech_stacks}

    # Resume
    {resume_details}

    # Standards
    아래 평가 기준에 부합하도록 지원자의 이력서를 평가하라.

    ## 핵심 심사 기준
    **직무 및 기술 적합성 (Role & Technical Alignment)** (총점 100점)
    - 회사의 비즈니스 도메인의 특성과 생태계를 이해하고 있는가? (총 25점)
    - 회사가 현재 사용 중인 핵심 기술 스택에 대한 실무 경험을 보유하고 있는가? 혹은 숙련도가 있거나, 높은 이해도와 빠른 학습 능력이 있는가? (25점)
    - 회사의 프로덕트와 유사한 아이템, 고객층, 규모, 복잡도의 제품 개발 경험이 있는가? (35점)
    - 개인 역량이 출중한가? (15점)

    ### 개인 역량 심사 기준 (총점 15점)
    **기술 역량 (Technical Competence)**
    - 비즈니스 요구사항을 이해하고, 이에 맞는 적절한 기술 스택과 아키텍처를 설계하여 기능을 구현한 경험 (1점)
    - 확장성과 안정성을 고려한 시스템 아키텍처 설계 및 구축 경험 (1점)
    - 클린 코드, 테스트 코드 작성 등 코드 품질 및 유지보수성에 대한 이해와 이를 실제 프로젝트에 적용한 사례 (1점)
    - 설계부터 개발, 테스트, 배포, 운영까지 제품의 End-to-End 생명 주기를 경험하고 개선해 본 이력 (1점)

    **문제 해결 및 실행력 (Problem-Solving & Execution)**
    - 문제의 현상 너머에 있는 핵심 원인을 파악하고, 이를 측정 가능한 구체적인 지표(Metric)로 정의하는 능력 (1점)
    - 정의된 문제를 해결하기 위해 논리적인 가설을 세우고, 작은 단위로 빠르게 실행하며 검증하는 사이클을 반복한 경험 (1점)
    - 기술적 난제나 복잡한 버그를 해결하여 비즈니스 또는 프로덕트 성과(예: 성능 개선, 비용 절감, 사용자 경험 향상)에 실질적으로 기여한 사례 (1점)

    **학습 및 성장 잠재력 (Learning & Growth Potential)**
    - 새로운 기술, 언어, 도메인에 대한 빠른 학습 능력과 이를 실제 프로젝트에 성공적으로 적용한 사례 (1점)
    - 기술 블로그 운영, 오픈소스 기여, 개인 프로젝트 진행, 세미나 발표 등 자기주도적 학습에 대한 꾸준한 노력과 결과물 (1점)
    - 경험한 실패를 회고하고 원인을 분석하여, 배운 점을 다음 프로젝트나 업무 방식에 적용하여 개선한 이력 (1점)

    **오너십 (Ownership)** (총점 100점)
    - 주어진 과업을 완수하는 것을 넘어, 스스로 문제를 발견하고 개선 방안을 적극적으로 제안하여 프로젝트를 주도한 경험 (1점)
    - 담당한 기능의 품질과 마일스톤에 대해 높은 책임감을 보이며, 예상치 못한 이슈 발생 시 해결을 위해 끝까지 노력한 사례 (1점)
    - 프로젝트의 성공을 자신의 일처럼 여기고, 팀의 목표 달성을 위해 필요하다면 명시된 역할 이상의 기여를 하려는 태도 (1점)

    **협업 및 소통 (Collaboration & Communication)** (총점 100점)
    - 기획, 디자인 등 다른 직군과 원활하게 소통하며 복잡한 요구사항을 조율하고 성공적으로 제품을 만들어낸 경험 (1점)
    - 기술적인 논의 과정에서 명확한 근거를 바탕으로 자신의 의견을 제시하고, 동시에 다른 팀원의 의견을 경청하여 더 나은 결론을 도출하는 능력 (0.5점)
    - 동료의 성장을 돕기 위해 코드 리뷰에 적극적으로 참여하거나, 팀 내에 지식을 공유하고 기술 문서를 작성한 이력 (0.5점)

    # Style
    ### 요소 및 순서
    보고서의 형식은 아래와 같은 순서의 요소들로 구성된다.

    **순서**
    0. 보고서 제목 ("xx포지션 경력직/신입 지원자 역량 평가 보고서", Heading 1로 작성)
    1. 종합 분석 결과
    2. 기준 별 세부 분석 (각 기준은 Heading 3로 작성)
    3. 피드백

    **요소 별 양식**
    - (0)은 "xx포지션 경력직/신입 지원자 서류 평가 보고서" 형식으로 작성, Heading 1로 작성
    - (1)은 핵심 심사 기준 점수 표, Heading 2로 작성
    - (2)는 핵심 심사 기준 세부 항목 점수 표와 근거로 구성, Heading 2로 작성하되, 각 기준은 Heading 3로 작성
    - (3)은 전반적인 지원자의 '강점 및 부각해야 할 점', '아쉽거나 부족한 점', '더 쌓아야 하는 경험', '이력서의 스토리텔링 제안,'으로 구성

    ### 표의 형식
    다음과 같은 Column Header를 지니는 Markdown Format의 표로 출력하라.
    1. 종합 분석 결과
    | 심사 결과 | 점수 |
    2. 기준 별 세부 분석
    | 세부 평가 기준 | 점수 |

    ### 문체
    보고서에 어울리는 격식 있는 문체로 작성하라.

    모든 사고 과정에서 '우리 회사에 어울리는 인재인지'를 최우선으로 판단하라.
    """

    return PromptTemplate(
        template=template,
        input_variables=[
            "company",
            "company_information",
            "introduction",
            "responsibilities",
            "qualification",
            "preference",
            "skills",
            "tech_stacks",
            "resume_details"
        ]
    )