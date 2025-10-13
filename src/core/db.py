# import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
# from psycopg_pool import AsyncConnectionPool
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver


@asynccontextmanager
async def lifespan_manager(app: FastAPI):
    """
    FastAPI lifespan Checkpointer.
    AgentState가 매 요청마다 초기화되지 않도록 해주는 역할
    - 서버 시작 시: DB와 연결된 Checkpointer를 생성하여 app.state에 저장
    - 1회의 DB 연결만으로 모든 요청 처리 가능
    """
    async with AsyncSqliteSaver.from_conn_string("checkpoint.sqlite") as checkpointer:
        app.state.checkpointer = checkpointer
        print("Checkpointer Ready.")
        yield
    print("Checkpointer Closed.")


# @asynccontextmanager
# async def lifespan_manager(app: FastAPI):
#     # 1. 환경 변수에서 DB URL 로드
#     DB_URL = os.environ.get("LANGGRAPH_DB_URL")
#     if not DB_URL:
#         raise RuntimeError("LANGGRAPH_DB_URL 환경 변수가 설정되지 않았습니다.")
    
#     # 2. 커넥션 풀 생성 및 앱 상태에 저장
#     pool = AsyncConnectionPool(conninfo=DB_URL, open=False, kwargs={"prepare_threshold": None})
#     await pool.open()
#     app.state.db_pool = pool
    
#     # 3. Checkpointer 생성 및 앱 상태에 저장
#     checkpointer = AsyncSqliteSaver(pool)
#     await checkpointer.setup()
#     app.state.checkpointer = checkpointer
    
#     print("Database pool and checkpointer are set up.")
    
#     try:
#         yield # 애플리케이션 실행
#     finally:
#         # 4. 앱 종료 시 자원 정리
#         await pool.close()
#         print("PostgreSQL Pool Closed.")
