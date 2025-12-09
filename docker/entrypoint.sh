#!/bin/sh
set -e

# Ensure the project directory points to the virtual environment for tooling that expects .venv
if [ -n "${VIRTUAL_ENV:-}" ] && [ ! -e "/app/.venv" ]; then
  ln -s "${VIRTUAL_ENV}" /app/.venv 2>/dev/null || true
fi

# Run database migrations unless explicitly skipped
if [ "${SKIP_MIGRATIONS:-0}" != "1" ]; then
  python manage.py migrate --noinput
else
  echo "SKIP_MIGRATIONS=1, skipping database migrations"
fi

exec "$@"
