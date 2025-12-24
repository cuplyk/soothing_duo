#!/bin/bash
set -e

echo "==> Environment check"
export PATH="/app/.venv/bin:$PATH"
echo "==> Using python: $(python --version)"
echo "==> Using gunicorn: $(gunicorn --version)"

echo "==> Database check..."
python -u manage.py check --database default

echo "==> Running migrations (verbose)..."
python -u manage.py migrate --noinput -v 2

echo "==> Starting Gunicorn on port $PORT..."
exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 200 \
    --log-level debug \
    --access-logfile - \
    --error-logfile -
