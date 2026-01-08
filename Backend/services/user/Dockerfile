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
        && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

WORKDIR /app

COPY libs/pyproject.toml libs/poetry.lock* /app/libs/
COPY services/user/pyproject.toml services/user/poetry.lock* /app/

RUN cd /app/libs && poetry install --no-root --only main && \
    cd /app && poetry install --no-root --only main --no-directory

# ==================== Runtime Stage ====================
FROM python:3.11-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.local/bin:$PATH"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 marigold && \
    mkdir -p /app/logs && \
    chown -R marigold:marigold /app

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY --chown=marigold:marigold libs /app/libs
COPY --chown=marigold:marigold services/user /app/services/user

USER marigold

WORKDIR /app/services/user

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${SERVICE_PORT:-8000}/health || exit 1

ENV SERVICE_PORT=8000

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--ws", "websockets"]
CMD ["--port", "8000"]