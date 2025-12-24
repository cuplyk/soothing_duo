# --- Build Stage ---
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Node.js
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Copy source
COPY . .

# Build Tailwind
WORKDIR /app/theme/static_src
RUN npm install && npm run build
WORKDIR /app

# Finalize venv and collect static
RUN uv sync --frozen --no-dev
RUN SECRET_KEY=dummy-key-for-build-purposes-only \
    DEBUG=False \
    DATABASE_URL=sqlite:///:memory: \
    uv run python manage.py collectstatic --no-input

# --- Final Runtime Stage ---
FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    # Add both the app and the venv bin to path
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Install runtime libs (libpq5 is for Postgres)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy uv binary so we can use 'uv run' if needed
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv

# Create user
RUN groupadd -g 1001 app && useradd -u 1001 -g app -s /bin/bash -m app

# Copy application (ensure staticfiles/ is included)
COPY --from=builder --chown=app:app /app /app

USER app

# Dynamic port binding for Railway
# Using 'exec' form within sh -c is the gold standard for Docker signals
CMD ["sh", "-c", "gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 2 --timeout 120 --log-level debug --access-logfile -"]