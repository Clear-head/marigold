# ==================== Build Stage ====================
FROM --platform=${BUILDPLATFORM:-linux/amd64} python:3.11-slim AS builder

ENV POETRY_VERSION=1.7.1 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        gcc \
        g++ \
        && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

WORKDIR /app

COPY libs/pyproject.toml libs/poetry.lock* /app/libs/
COPY services/ai/pyproject.toml services/ai/poetry.lock* /app/

# AI 라이브러리는 빌드 시간이 오래 걸리므로 타임아웃 증가
RUN cd /app/libs && poetry install --no-root --only main && \
    cd /app && poetry install --no-root --only main --no-directory

# ==================== Runtime Stage ====================
FROM python:3.11-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.local/bin:$PATH" \
    # LangChain 최적화
    LANGCHAIN_TRACING_V2=false \
    TOKENIZERS_PARALLELISM=false

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        libgomp1 \
        && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 marigold && \
    mkdir -p /app/logs /app/cache && \
    chown -R marigold:marigold /app

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY --chown=marigold:marigold libs /app/libs
COPY --chown=marigold:marigold services/ai /app/services/ai

USER marigold

WORKDIR /app/services/ai

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${SERVICE_PORT:-8000}/health || exit 1

ENV SERVICE_PORT=8000

# AI 서비스는 더 많은 워커와 타임아웃 필요
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--timeout-keep-alive", "75"]
CMD ["--port", "8000"]