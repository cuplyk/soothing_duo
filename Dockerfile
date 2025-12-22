# --- Build Stage ---
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Set build-time environment variables
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install Node.js (needed for Tailwind CSS build)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies first for better caching
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the source code
COPY . .

# Build Tailwind CSS
# Assuming the tailwind app is named 'theme' and static_src is inside it
WORKDIR /app/theme/static_src
RUN npm install && npm run build
WORKDIR /app

# Build the project (finalizes the .venv)
RUN uv sync --frozen --no-dev

# Run collectstatic with dummy environment variables
# We use DATABASE_URL=sqlite:///:memory: to avoid needing a real DB during build
RUN SECRET_KEY=dummy-key-for-build-purposes-only \
    DEBUG=False \
    DATABASE_URL=sqlite:///:memory: \
    uv run python manage.py collectstatic --no-input

# Clean up build-only files to keep the final image slim
RUN rm -rf theme/static_src/node_modules

# --- Final Runtime Stage ---
FROM python:3.12-slim-bookworm

# Set runtime environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    PORT=8080

WORKDIR /app

# Install runtime system dependencies (if any)
# For example, libpq might be needed if not using psycopg2-binary
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     libpq5 \
#     && rm -rf /var/lib/apt/lists/*

# Create a non-privileged user to run the app
RUN groupadd -g 1001 app && \
    useradd -u 1001 -g app -s /bin/bash -m app

# Copy the application from the builder stage
COPY --from=builder --chown=app:app /app /app

# Switch to the non-privileged user
USER app

# Document the port the container listens on
EXPOSE 8080

# The actual start command is often overridden in railway.json
# But we provide a sensible default here
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120"]