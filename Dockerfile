FROM ghcr.io/docling-project/docling-serve-cpu:latest

WORKDIR /app

COPY pyproject.toml .

RUN uv pip sync --system pyproject.toml

COPY ./src ./src

LABEL org.opencontainers.image.source=https://github.com/C-fit/c-fit-llm-python-backend

EXPOSE 8080

CMD uvicorn src.server:app --host 0.0.0.0 --port ${PORT:-8080}
