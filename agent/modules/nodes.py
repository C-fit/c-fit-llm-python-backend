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

from agent.utils.base_node import BaseNode
import agent.modules.chains as chains
from agent.modules.states import AgentState
import agent.modules.prompts as prompts

from dotenv import load_dotenv
load_dotenv()

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
        self.prompt = prompts.get_resume_prompt(AgentState)
        self.chain = chains.set_decomposition_chain(self.prompt)

    def execute(self, state: AgentState) -> dict:
        prompt_chain = self.chain
        response = prompt_chain.invoke(
            {
                "resume": state["resume"]
                # "position": state["resume"]["position"],
                # "tech_stacks": state["resume"]["tech_stacks"],
                # "years": state["resume"]["years"],
                # "awards": state["resume"]["awards"],
                # "certifications": state["resume"]["certifications"],
                # "etcetra": state["resume"]["etcetra"],
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
        self.prompt = prompts.get_experiences_prompt(AgentState)
        self.chain = chains.set_decomposition_chain(self.prompt)

    def execute(self, state: AgentState) -> dict:
        prompt_chain = self.chain
        response = prompt_chain.invoke(
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
        self.prompt = prompts.get_projects_prompt(AgentState)
        self.chain = chains.set_decomposition_chain(self.prompt)

    def execute(self, state: AgentState) -> dict:
        prompt_chain = self.chain
        response = prompt_chain.invoke(
            {
                "resume": state["resume"]
            }
        )
        result = json_repair.loads(response)

        # resume_details에서 is_hired 값 확인
        current_resume_details = state.get("resume_details", {})
        is_hired = current_resume_details.get("is_hired", False)
        
        if is_hired:
            # 경력자인 경우: experiences 하위에 projects 저장
            return {"resume_details": {"experiences": {"projects": result}}}
        else:
            # 신입인 경우: resume_details 직속에 projects 저장
            return {"resume_details": {"projects": result}}


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
        self.prompt = prompts.get_experiences_prompt(AgentState)
        self.chain = chains.set_decomposition_chain(self.prompt)

    def execute(self, state: AgentState) -> dict:
        prompt_chain = self.chain
        response = prompt_chain.invoke(
            {
                "job_description": state["job_description"]
            }
        )
        result = json_repair.loads(response)
        return {"jd_details": result}