from langgraph.graph import StateGraph

from src.agent.utils.base_workflow import BaseWorkflow
from src.agent.modules.states import AgentState
import src.agent.modules.nodes as nd


class MainWorkflow(BaseWorkflow):
    """
    메인 Workflow 클래스
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
        StateGraph를 사용하여 Workflow 그래프 구축

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

        # workflow = builder.compile()  # 그래프 컴파일
        builder.name = self.name  # Workflow 이름 설정
        return builder
    

class PreprocessResumeWorkflow(BaseWorkflow):
    """
    이력서 전처리 Workflow
    """
    def __init__(self, state):
        super().__init__()
        self.state = state

    def build(self):
        builder = StateGraph(self.state)

        # 이력서 PDF 및 채용공고 URL 전처리 노드
        builder.add_node("extract_resume", nd.ResumePdfToMarkdownNode())

        # 이력서 전처리 노드
        builder.add_node("decompose_resume", nd.ResumeDecompositionNode())
        builder.add_node("decompose_experiences", nd.ResumeExperiencesNode())
        builder.add_node("decompose_projects", nd.ResumeProjectsNode())
        builder.add_node("extract_company_projects", nd.ResumeCompanyProjectsNode())

        # 그래프 연결
        builder.add_edge("__start__", "extract_resume")

        builder.add_edge("extract_resume", "decompose_resume")
        builder.add_edge("decompose_resume", "decompose_experiences")
        builder.add_edge("decompose_experiences", "decompose_projects")
        builder.add_edge("decompose_projects", "extract_company_projects")

        builder.add_edge("extract_company_projects", "__end__")

        # workflow = builder.compile()  # 그래프 컴파일
        builder.name = self.name  # Workflow 이름 설정
        return builder


class PreprocessJDWorkflow(BaseWorkflow):
    """
    채용공고 전처리 Workflow
    """

    def __init__(self, state):
        super().__init__()
        self.state = state

    def build(self):
        builder = StateGraph(self.state)

        # JD 전처리 노드
        builder.add_node("extract_jd", nd.JDUrlToMarkdown())
        builder.add_node("decompose_jd", nd.JDDecompositionNode())

        # 그래프 연결
        builder.add_edge("__start__", "extract_jd")
        builder.add_edge("extract_jd", "decompose_jd")
        builder.add_edge("decompose_jd", "__end__")

        # workflow = builder.compile()  # 그래프 컴파일
        builder.name = self.name  # Workflow 이름 설정
        return builder
    

class AnalyzeResumeWorkflow(BaseWorkflow):
    """
    이력서 분석 Workflow
    """

    def __init__(self, state):
        super().__init__()
        self.state = state

    def build(self):
        builder = StateGraph(self.state)

        # 평가 노드
        builder.add_node("evaluate_skills", nd.EvaluateSkillsNode())

        # 그래프 연결
        builder.add_edge("__start__", "evaluate_skills")
        builder.add_edge("evaluate_skills", "__end__")

        # workflow = builder.compile()  # 그래프 컴파일
        builder.name = self.name  # Workflow 이름 설정
        return builder
    

class AnalyzeRecruitWorkflow(BaseWorkflow):
    """
    이력서 && JD 비교 분석 Workflow
    """

    def __init__(self, state):
        super().__init__()
        self.state = state

    def build(self):
        builder = StateGraph(self.state)

        # 평가 노드
        builder.add_node("evaluate_recruitment", nd.EvaluateRecruitlNode())

        # 그래프 연결
        builder.add_edge("__start__", "evaluate_recruitment")
        builder.add_edge("evaluate_recruitment", "__end__")

        # workflow = builder.compile()  # 그래프 컴파일
        builder.name = self.name  # Workflow 이름 설정
        return builder


# initial_state = {
#     "resume_file": "/home/catusciows/workspace/c-fit/pdf/이력서.pdf",
#     "jd_url": "https://www.wanted.co.kr/wd/290088"
# }

# main_workflow = MainWorkflow(AgentState)
# work = main_workflow.build()
# result = work.invoke(initial_state)

# print(result)