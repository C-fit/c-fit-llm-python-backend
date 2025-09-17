from typing import Literal
from langchain_core.messages import AIMessage
from agent.modules.states import AgentState


def router(state) -> Literal["__end__", "tools"]:
    """
    모델의 출력을 기반으로 다음 노드를 결정하는 라우터 함수

    이 함수는 LLM의 마지막 메시지를 검사하여 도구 호출이 포함되어 있는지 확인하고,
    그 결과에 따라 Workflow의 다음 단계를 결정합니다.

    도구 호출이 있으면 "tools" 노드로 라우팅하고, 그렇지 않으면 Workflow를 종료합니다.
    이는 ReAct 패턴의 일반적인 구현 방식으로, LLM이 도구를 사용해야 할지 또는
    최종 응답을 생성해야 할지를 결정하게 합니다.

    Args:
        state (State): 현재 Workflow 상태 객체 (메시지 기록 포함)

    Returns:
        str: 다음에 실행할 노드의 이름 ("__end__" 또는 "tools")

    Raises:
        ValueError: 마지막 메시지가 AIMessage 타입이 아닌 경우

    예시:
    ```python
    # Workflow에 조건부 에지 추가
    builder.add_conditional_edges(
        "call_model",  # 소스 노드
        router,       # 라우터 함수
        {
            "__end__": "__end__",  # 종료 조건
            "tools": "execute_tools"  # 도구 실행 조건
        }
    )
    ```
    """
    # 상태에서 마지막 메시지 가져오기
    last_message = state.messages[-1]

    # 메시지 타입 검증
    if not isinstance(last_message, AIMessage):
        raise ValueError(
            f"Expected AIMessage in output edges, but got {type(last_message).__name__}"
        )

    # 도구 호출 여부에 따른 라우팅 결정
    if not last_message.tool_calls:
        return "__end__"  # 도구 호출이 없으면 Workflow 종료

    # 도구 호출이 있으면 도구 실행 노드로 라우팅
    return "tools"


def is_experience_router(state: AgentState):
    """
    AgentState의 값에 따른 라우팅
    """
    # storyboard에서 includes_human 값 확인
    is_hired = state.get('resume_details', {}).get('is_hired', False)
    
    if is_hired:
        print("=" * 20, "\nCurrent Node: Router Node")
        print("-> is_hired: True; 경력직입니다.")
        return ["set_background", "set_style"]  # 사람이 포함된 경우 모델 설정 노드와 병렬
    else:
        print("=" * 20, "\nCurrent Node: Router Node")
        print("-> includes_human: False; 신입입니다.")
        return "set_background"     # 포함되지 않은 경우 human 노드 제외
    