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


# Resume 분해
class ResumeDecompositionNode(BaseNode):
    """
    이력서 내용을 분해하는 노드

    Args:
        이력서 str
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prompt = prompts.get_resume_prompt(AgentState)
        self.chain = chains.set_resume_chain(self.prompt)

    def execute(self, state: AgentState) -> dict:
        prompt_chain = self.chain
        response = prompt_chain.invoke(
            {
                "position": state["resume"]["position"],
                "tech_stacks": state["resume"]["tech_stacks"],
                "years": state["resume"]["years"],
                "awards": state["resume"]["awards"],
                "certifications": state["resume"]["certifications"],
                "etcetra": state["resume"]["etcetra"],
            }
        )
        result = json_repair.loads(response)
        return {"resume_details": result}