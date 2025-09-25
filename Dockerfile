FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml .

RUN uv pip install --system \
    torch \
    torchvision \
    --extra-index-url https://download.pytorch.org/whl/cpu

RUN uv pip sync --system pyproject.toml

COPY ./src ./src

LABEL org.opencontainers.image.source=https://github.com/C-fit/c-fit-llm-python-backend

EXPOSE 8080

CMD uvicorn src.server:app --host 0.0.0.0 --port ${PORT:-8080}
