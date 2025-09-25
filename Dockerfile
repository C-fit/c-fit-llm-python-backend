FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml .

RUN uv pip install --system torch --extra-index-url https://download.pytorch.org/whl/cpu && \
    uv pip sync --system pyproject.toml

COPY ./src ./src

LABEL org.opencontainers.image.source="https://github.com/C-fit/c-fit-llm-python-backend"

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000"]
