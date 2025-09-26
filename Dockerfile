FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml .

RUN uv pip install --system \
    -r pyproject.toml 

COPY ./src ./src

EXPOSE 8080

CMD uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8080}