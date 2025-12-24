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
WORKDIR /app/theme/static_src
RUN npm install && npm run build
WORKDIR /app

# Build the project (finalizes the .venv)
RUN uv sync --frozen --no-dev

# Run collectstatic with dummy environment variables
# Ensure STATIC_ROOT in settings.py points to /app/staticfiles
RUN SECRET_KEY=dummy-key-for-build-purposes-only \
    DEBUG=False \
    DATABASE_URL=sqlite:///:memory: \
    uv run python manage.py collectstatic --no-input

# Clean up build-only files
RUN rm -rf theme/static_src/node_modules

# --- Final Runtime Stage ---
FROM python:3.12-slim-bookworm

# Set runtime environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # This ensures the python from the builder's venv is used
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Install minimal runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Create a non-privileged user
RUN groupadd -g 1001 app && \
    useradd -u 1001 -g app -s /bin/bash -m app

# Copy the application and the virtual environment from builder
COPY --from=builder --chown=app:app /app /app

# Ensure scripts are executable
RUN chmod +x /app/scripts/start.sh

# Switch to the non-privileged user
USER app

# Railway ignores EXPOSE, but it's good practice for documentation
EXPOSE 8080

# Use the start script
CMD ["/app/scripts/start.sh"]