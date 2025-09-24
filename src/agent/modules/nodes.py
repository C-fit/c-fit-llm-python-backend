"""
노드 클래스 모듈

해당 클래스 모듈은 각각 노드 클래스가 BaseNode를 상속받아 노드 클래스를 구현하는 모듈입니다.
"""

import os
import base64
import json
import json_repair
from typing import Dict, Any

from langchain_core.runnables import RunnableSerializable
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from src.agent.utils.base_node import BaseNode
import src.agent.modules.chains as chains
from src.agent.modules.states import AgentState
import src.agent.modules.prompts as prompts

from src.preprocess.pdf_loader import load_pdf
from src.preprocess.url_loader import load_url

from dotenv import load_dotenv
load_dotenv()


"""
Step 0. 전처리
"""
class ResumePdfToMarkdownNode(BaseNode):
    """이력서 pdf 파일을 markdown으로 변환하는 노드

    Args:
        resume_file (str): 이력서 파일 경로

    Returns:
        resume (str): 이력서 전문 markdown text
    """
    async def execute(self, state: AgentState) -> dict:
        result = load_pdf(state["resume_file"])
        return {"resume": result}
    

class JDUrlToMarkdown(BaseNode):
    """JD URL을 markdown으로 변환하는 노드

    Args:
        jd_url (str): 채용 공고 URL

    Returns:
        job_description (str): 채용공고 전문 markdown text
    """
    async def execute(self, state: AgentState) -> dict:
        result = load_url(state["jd_url"])
        return {"job_description": result}
    

"""
Step 1. 이력서 관련 노드
"""
class ResumeDecompositionNode(BaseNode):
    """이력서 내용을 분해하는 노드

    Args:
        resume (str): 이력서 전체 string

    Returns:
        resume_details (TypedDict): 이력서 분해 결과
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prompt = prompts.get_resume_prompt()
        self.chain = chains.set_decomposition_chain(self.prompt)

    async def execute(self, state: AgentState) -> dict:
        prompt_chain = self.chain
        response = await prompt_chain.ainvoke(
            {
                "resume": state["resume"]
            }
        )
        result = json_repair.loads(response)
        return {"resume_details": result}


class ResumeExperiencesNode(BaseNode):
    """이력서에서 경력(직장 및 프로젝트)을 추출하는 노드

    Args:
        resume (str): 이력서 전체 string

    Returns:
        resume_details (TypedDict): 이력서 분해 결과
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prompt = prompts.get_experiences_prompt()
        self.chain = chains.set_decomposition_chain(self.prompt)

    async def execute(self, state: AgentState) -> dict:
        prompt_chain = self.chain
        response = await prompt_chain.ainvoke(
            {
                "resume": state["resume"]
            }
        )
        result = json_repair.loads(response)
        return {"resume_details": {"experiences": result}}


class ResumeProjectsNode(BaseNode):
    """이력서에서 프로젝트를 추출하는 노드

    Args:
        resume (str): 이력서 전체 string

    Returns:
        resume_details (TypedDict): 이력서 분해 결과
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prompt = prompts.get_projects_prompt()
        self.chain = chains.set_decomposition_chain(self.prompt)

    async def execute(self, state: AgentState) -> dict:
        prompt_chain = self.chain
        response = await prompt_chain.ainvoke(
            {
                "resume": state["resume"]
            }
        )
        result = json_repair.loads(response)

        return{"resume_details": {"projects": result}}


class ResumeCompanyProjectsNode(BaseNode):
    """프로젝트 목록에서 회사 프로젝트만 추출하는 노드

    Args:
        projects (TypedDict): 진행한 프로젝트 목록

    Returns:
        resume_details (TypedDict): 이력서 분해 결과
    """    
    async def execute(self, state: AgentState) -> dict:
        # .get()을 사용하여 키가 없는 경우에도 에러가 나지 않도록 함
        projects = state.get("resume_details", {}).get("projects", [])
        experiences = state.get("resume_details", {}).get("experiences", [])

        # 1. experiences가 리스트가 아닐 경우를 대비한 방어 코드
        if not isinstance(experiences, list):
            # 비정상적인 입력이므로, 빈 리스트로 처리하고 넘어감
            experiences = []
        
        experiences_dict = {}
        remaining_projects = []

        # 2. 리스트의 각 요소가 딕셔너리인지 확인하는 방어 코드
        for exp in experiences:
            # exp가 딕셔너리이고 'company' 키를 가지고 있을 때만 처리
            if isinstance(exp, dict) and 'company' in exp:
                experiences_dict[exp['company']] = exp
            else:
                # 딕셔너리가 아닌 요소(예: 문자열)는 무시하고 넘어감
                if self.verbose:
                    print(f"Skipping invalid experience item: {exp}")

        # projects 리스트 순회 시에도 동일한 방어 코드 적용
        for project in projects:
            if not isinstance(project, dict):
                if self.verbose:
                    print(f"Skipping invalid project item: {project}")
                continue # 딕셔너리가 아니면 건너뜀

            project_company = project.get('company')

            if project_company and project_company in experiences_dict:
                if 'projects' not in experiences_dict[project_company]:
                    experiences_dict[project_company]['projects'] = []
                experiences_dict[project_company]['projects'].append(project)
            else:
                remaining_projects.append(project)

        updated_experiences = list(experiences_dict.values())

        return {
            "resume_details": {
                "projects": remaining_projects,
                "experiences": updated_experiences
            }
        }



"""
JD 관련 노드
"""
class JDDecompositionNode(BaseNode):
    """채용공고(JD)에서 정보를 추출하는 노드

    Args:
        job_description (str): 채용공고 전체 string

    Returns:
        jd_details (TypedDict): 채용공고 분해 결과
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prompt = prompts.get_jd_prompt()
        self.chain = chains.set_jd_chain(self.prompt)

    async def execute(self, state: AgentState) -> dict:
        prompt_chain = self.chain
        response = await prompt_chain.ainvoke(
            {
                "job_description": state["job_description"]
            }
        )
        result = json_repair.loads(response)
        return {"jd_details": result}
    

"""
평가 관련 노드
"""
class EvaluateSkillsNode(BaseNode):
    """이력서를 토대로 지원자의 역량을 평가하는 노드

    Args:
        resume_details (TypedDict): 이력서 분해 결과

    Returns:
        applicant_skills (str): 이력서 평가 결과
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prompt = prompts.get_skills_analysis_prompt()
        self.chain = chains.set_resume_evaluation_chain(self.prompt)

    async def execute(self, state: AgentState) -> dict:
        prompt_chain = self.chain
        response = await prompt_chain.ainvoke(
            {
                "resume_details": state["resume_details"]
            }
        )
        # result = json_repair.loads(response)

        return{"applicant_skills": response}
    

class EvaluateRecruitlNode(BaseNode):
    """이력서와 JD를 토대로 지원자의 역량을 평가하는 노드

    Args:
        resume_details (TypedDict): 이력서 분해 결과

    Returns:
        applicant_skills (str): 이력서 평가 결과
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prompt = prompts.get_recruit_analysis_prompt()
        self.chain = chains.set_recruit_evaluation_chain(self.prompt)

    async def execute(self, state: AgentState) -> dict:
        prompt_chain = self.chain
        response = await prompt_chain.ainvoke(
            {
                "company": state["jd_details"]["company"],
                "company_information": state["jd_details"]["company_information"],
                "title": state["jd_details"]["title"],
                "introduction": state["jd_details"]["introduction"],
                "responsibilities": state["jd_details"]["responsibilities"],
                "qualification": state["jd_details"]["qualification"],
                "preference": state["jd_details"]["preference"],
                "skills": state["jd_details"]["skills"],
                "tech_stacks": state["jd_details"]["tech_stacks"],
                "resume_details": state["resume_details"]
            }
        )
        # result = json_repair.loads(response)

        return{"applicant_recruitment": response}