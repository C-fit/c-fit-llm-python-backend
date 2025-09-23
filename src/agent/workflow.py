from langgraph.graph import StateGraph

from src.agent.utils.base_workflow import BaseWorkflow
from src.agent.utils.main_state import MainState
from src.agent.modules.states import AgentState
import src.agent.modules.nodes as nd


class MainWorkflow(BaseWorkflow):
    """
    메인 Workflow 클래스

    Team Member는 해당 Workflow에서 따로 작업을 진행하지 않으셔도 됩니다.
    이 클래스는 모든 Agentic Workflow를 바탕으로 주요 Workflow를 정의합니다.
    """

    def __init__(self, state):
        """
        Args:
            state (StateGraph): Workflow에서 사용할 상태 클래스
        """
        super().__init__()
        self.state = state

    def build(self):
        """
        Workflow 그래프 구축 메서드

        StateGraph를 사용하여 Workflow 그래프를 구축합니다.
        추후 다양한 노드를 추가하여 최종 Workflow를 구축할 예정입니다.

        Returns:
            CompiledStateGraph: 컴파일된 상태 그래프 객체
        """
        builder = StateGraph(self.state)

        # 이력서 PDF 및 채용공고 URL 전처리 노드
        builder.add_node("extract_resume", nd.ResumePdfToMarkdownNode())
        builder.add_node("extract_jd", nd.JDUrlToMarkdown())

        # 이력서 전처리 노드
        builder.add_node("decompose_resume", nd.ResumeDecompositionNode())
        builder.add_node("decompose_experiences", nd.ResumeExperiencesNode())
        builder.add_node("decompose_projects", nd.ResumeProjectsNode())
        builder.add_node("extract_company_projects", nd.ResumeCompanyProjectsNode())

        # JD 전처리 노드
        builder.add_node("decompose_jd", nd.JDDecompositionNode())

        # 평가 노드
        builder.add_node("evaluate_skills", nd.EvaluateSkillsNode())
        builder.add_node("evaluate_recruitment", nd.EvaluateRecruitlNode())

        # 그래프 연결
        builder.add_edge("__start__", "extract_resume")
        builder.add_edge("__start__", "extract_jd")

        builder.add_edge("extract_resume", "decompose_resume")
        builder.add_edge("decompose_resume", "decompose_experiences")
        builder.add_edge("decompose_experiences", "decompose_projects")
        builder.add_edge("decompose_projects", "extract_company_projects")
        # builder.add_edge("extract_company_projects", "evaluate_skills")
        builder.add_edge("extract_company_projects", "evaluate_recruitment")

        builder.add_edge("extract_jd", "decompose_jd")
        # builder.add_edge("decompose_jd", "evaluate_skills")
        builder.add_edge("decompose_jd", "evaluate_recruitment")

        # builder.add_edge("extract_company_projects", "__end__")
        # builder.add_edge("evaluate_skills", "__end__")
        builder.add_edge("evaluate_recruitment", "__end__")

        workflow = builder.compile()  # 그래프 컴파일
        workflow.name = self.name  # Workflow 이름 설정
        return workflow


initial_state = {
    "resume_file": "/home/catusciows/workspace/c-fit/pdf/이력서.pdf",
    "jd_url": "https://www.wanted.co.kr/wd/290088"
}

main_workflow = MainWorkflow(AgentState)
work = main_workflow.build()
result = work.invoke(initial_state)

print(result)