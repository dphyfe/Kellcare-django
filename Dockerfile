# syntax=docker/dockerfile:1

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_ROOT_USER_ACTION=ignore

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

COPY requirements.txt ./

RUN python -m venv "$VIRTUAL_ENV" \
    && "$VIRTUAL_ENV/bin/pip" install --upgrade pip \
    && "$VIRTUAL_ENV/bin/pip" install --no-cache-dir -r requirements.txt

RUN apt-get update \
    && apt-get install -y --no-install-recommends libcap2-bin \
    && CAP_TARGET="$(readlink -f "$VIRTUAL_ENV/bin/python3.11")" \
    && echo "Setting capability on ${CAP_TARGET}" \
    && setcap 'cap_net_bind_service=+ep' "${CAP_TARGET}" \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /app \
    && chmod +x docker/entrypoint.sh

USER appuser

EXPOSE 80

ENTRYPOINT ["./docker/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
