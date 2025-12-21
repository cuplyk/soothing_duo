# Use uv for fast dependency management
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Install Node.js for Tailwind CSS build
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# Install Python dependencies first (layer caching)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Copy project files
COPY . /app

# Build Tailwind CSS
WORKDIR /app/theme/static_src
RUN npm install && npm run build

# Finalize uv sync with the actual project
WORKDIR /app
RUN uv sync --frozen --no-dev

# Collect static files
# Mock environment variables for the build-time collection
RUN SECRET_KEY=build-time-secret-key-12345 \
    DEBUG=False \
    DATABASE_URL=sqlite:///:memory: \
    uv run python manage.py collectstatic --no-input


# --- Final Image ---
FROM python:3.12-slim-bookworm

WORKDIR /app

# Create a non-root user for security
RUN groupadd -r app && useradd -r -g app app

# Copy the application and virtual environment from the builder
COPY --from=builder --chown=app:app /app /app

# Set production environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
# Default port if not provided by Railway
ENV PORT=8080

# Switch to the non-root user
USER app

# Expose the default port (documentation only)
EXPOSE 8080

# Start gunicorn, binding to the dynamic PORT provided by Railway
# We use the shell form to allow variable expansion of $PORT
CMD gunicorn core.wsgi:application --bind 0.0.0.0:${PORT} --workers 2