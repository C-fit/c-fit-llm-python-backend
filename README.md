# C:fit LLM / Python Backend
C:fit의 LLM 에이전트 로직과 백엔드 로직이 담긴 Repo 입니다.

# How to
1. 이 Repo를 `git clone` 합니다.
2. uv를 설치하고 아래 명령어를 터미널에 입력합니다.
    ```
    cd c-fit-llm-python-backend
    uv sync
    ```
3. 작업 시
    ```
    source .venv/bin/activate
    ```
    로 가상환경 진입 후 작업합니다. Windows의 경우,
    ```
    source .venv\Scripts\activate
    ```
로 사용할 수 있습니다.

가상환경은 `deactivate` 명령어로 중지 가능합니다.

해당 Repo의 Agent 기능 구현은 Proact0의 Act Template을 기반으로 구현되었습니다.
https://github.com/Proact0/Act-Template