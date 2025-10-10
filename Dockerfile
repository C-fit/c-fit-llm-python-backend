FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml .

RUN uv pip install --system \
    -r pyproject.toml 

COPY ./src ./src

# 환경변수 설정
ENV PORT=8000

EXPOSE $PORT

# 환경변수 사용
CMD uvicorn src.main:app --host 0.0.0.0 --port $PORT