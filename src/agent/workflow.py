"""LLM Agent Workflow 모듈
Task 별 Multi-Agent Workflow를 정의합니다.
"""
from langgraph.graph import StateGraph

from src.agent.utils.base_workflow import BaseWorkflow
from src.agent.modules.states import AgentState
import src.agent.modules.nodes as nd


class OneclickResumeWorkflow(BaseWorkflow):
    """
    원클릭 이력서 분석 워크플로우
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

        # 이력서 전처리 노드
        builder.add_node("decompose_resume", nd.ResumeDecompositionNode())
        builder.add_node("decompose_experiences", nd.ResumeExperiencesNode())
        builder.add_node("decompose_projects", nd.ResumeProjectsNode())
        builder.add_node("extract_company_projects", nd.ResumeCompanyProjectsNode())

        # 평가 노드
        builder.add_node("evaluate_resume", nd.EvaluateResumeNode())

        # 그래프 연결
        builder.add_edge("__start__", "decompose_resume")
        builder.add_edge("decompose_resume", "decompose_experiences")
        builder.add_edge("decompose_experiences", "decompose_projects")
        builder.add_edge("decompose_projects", "extract_company_projects")
        builder.add_edge("extract_company_projects", "evaluate_resume")
        builder.add_edge("evaluate_resume", "__end__")

        # workflow = builder.compile()  # 그래프 컴파일
        builder.name = self.name  # Workflow 이름 설정
        return builder


class OneclickFitWorkflow(BaseWorkflow):
    """
    원클릭 Fit 워크플로우
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
        builder.add_node("extract_jd", nd.JDUrlToMarkdown())

        # 이력서 전처리 노드
        builder.add_node("decompose_resume", nd.ResumeDecompositionNode())
        builder.add_node("decompose_experiences", nd.ResumeExperiencesNode())
        builder.add_node("decompose_projects", nd.ResumeProjectsNode())
        builder.add_node("extract_company_projects", nd.ResumeCompanyProjectsNode())

        # JD 전처리 노드
        builder.add_node("decompose_jd", nd.JDDecompositionNode())

        # 평가 노드
        builder.add_node("evaluate_resume", nd.EvaluateResumeNode())
        builder.add_node("evaluate_fit", nd.EvaluateFitNode())

        # 레포트 노드
        builder.add_node("standard_analysis", nd.StandardAnalysisNode())
        builder.add_node("deep_dives_analysis", nd.DeepDivesNode())
        builder.add_node("overall_analysis", nd.OverallEvaluationNode())

        builder.add_node("formatter", nd.IntegrateContextNode())

        # 그래프 연결
        builder.add_edge("__start__", "decompose_resume")
        builder.add_edge("__start__", "extract_jd")

        # 이력서 파이프라인
        builder.add_edge("decompose_resume", "decompose_experiences")
        builder.add_edge("decompose_experiences", "decompose_projects")
        builder.add_edge("decompose_projects", "extract_company_projects")
        builder.add_edge("extract_company_projects", "evaluate_fit")

        # JD 파이프라인
        builder.add_edge("extract_jd", "decompose_jd")

        builder.add_edge("decompose_jd", "standard_analysis")
        builder.add_edge("decompose_jd", "deep_dives_analysis")

        # 레포트 파이프라인
        builder.add_edge("deep_dives_analysis", "overall_analysis")
        builder.add_edge("deep_dives_analysis", "overall_analysis")
        builder.add_edge("overall_analysis", "formatter")
        builder.add_edge("formatter", "__end__")

        # workflow = builder.compile()  # 그래프 컴파일
        builder.name = self.name  # Workflow 이름 설정
        return builder

# class OneclickFitWorkflow(BaseWorkflow): 
#     """
#     원클릭 Fit 워크플로우
#     """

#     def __init__(self, state):
#         """
#         Args:
#             state (StateGraph): Workflow에서 사용할 상태 클래스
#         """
#         super().__init__()
#         self.state = state

#     def build(self):
#         """
#         StateGraph를 사용하여 Workflow 그래프 구축

#         Returns:
#             CompiledStateGraph: 컴파일된 상태 그래프 객체
#         """
#         builder = StateGraph(self.state)

#         # 이력서 PDF 및 채용공고 URL 전처리 노드
#         builder.add_node("extract_jd", nd.JDUrlToMarkdown())

#         # 이력서 전처리 노드
#         builder.add_node("decompose_resume", nd.ResumeDecompositionNode())
#         builder.add_node("decompose_experiences", nd.ResumeExperiencesNode())
#         builder.add_node("decompose_projects", nd.ResumeProjectsNode())
#         builder.add_node("extract_company_projects", nd.ResumeCompanyProjectsNode())

#         # JD 전처리 노드
#         builder.add_node("decompose_jd", nd.JDDecompositionNode())

#         # 평가 노드
#         builder.add_node("evaluate_resume", nd.EvaluateResumeNode())
#         builder.add_node("evaluate_fit", nd.EvaluateFitNode())

#         # 그래프 연결
#         builder.add_edge("__start__", "decompose_resume")
#         builder.add_edge("__start__", "extract_jd")

#         # 이력서 파이프라인
#         builder.add_edge("decompose_resume", "decompose_experiences")
#         builder.add_edge("decompose_experiences", "decompose_projects")
#         builder.add_edge("decompose_projects", "extract_company_projects")
#         builder.add_edge("extract_company_projects", "evaluate_fit")

#         # JD 파이프라인
#         builder.add_edge("extract_jd", "decompose_jd")
#         builder.add_edge("decompose_jd", "evaluate_fit")

#         builder.add_edge("evaluate_fit", "__end__")

#         # workflow = builder.compile()  # 그래프 컴파일
#         builder.name = self.name  # Workflow 이름 설정
#         return builder


class PreprocessResumeWorkflow(BaseWorkflow):
    """
    이력서 전처리 Workflow
    """
    def __init__(self, state):
        super().__init__()
        self.state = state

    def build(self):
        builder = StateGraph(self.state)

        # 이력서 전처리 노드
        builder.add_node("decompose_resume", nd.ResumeDecompositionNode())
        builder.add_node("decompose_experiences", nd.ResumeExperiencesNode())
        builder.add_node("decompose_projects", nd.ResumeProjectsNode())
        builder.add_node("extract_company_projects", nd.ResumeCompanyProjectsNode())

        # 그래프 연결
        builder.add_edge("__start__", "decompose_resume")
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
        builder.add_node("evaluate_resume", nd.EvaluateResumeNode())

        # 그래프 연결
        builder.add_edge("__start__", "evaluate_resume")
        builder.add_edge("evaluate_resume", "__end__")

        # workflow = builder.compile()  # 그래프 컴파일
        builder.name = self.name  # Workflow 이름 설정
        return builder
    

class AnalyzeFitWorkflow(BaseWorkflow):
    """
    이력서 && JD 비교 분석 Workflow
    """

    def __init__(self, state):
        super().__init__()
        self.state = state

    def build(self):
        builder = StateGraph(self.state)

        # 평가 노드
        builder.add_node("evaluate_fit", nd.EvaluateFitNode())

        # 그래프 연결
        builder.add_edge("__start__", "evaluate_fit")
        builder.add_edge("evaluate_fit", "__end__")

        # workflow = builder.compile()  # 그래프 컴파일
        builder.name = self.name  # Workflow 이름 설정
        return builder
