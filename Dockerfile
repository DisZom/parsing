FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false

RUN pip install --upgrade pip && pip install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN poetry install --without dev --no-root --no-interaction --no-ansi
COPY .env app/ ./

CMD [ "celery", "-A", "tasks", "worker", "-l", "INFO", "-P", "gevent" ]
