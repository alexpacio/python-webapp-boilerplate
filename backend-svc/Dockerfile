FROM python:3.12.6-bookworm
EXPOSE 8000

ENV POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=1 \
  POETRY_CACHE_DIR='/tmp/poetry_cache'

# System deps:
RUN pip install poetry==1.8.3

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY poetry.lock pyproject.toml pytest.ini /app/

# Project initialization:
RUN poetry install --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY src /app/src/
COPY tests /app/tests/

SHELL ["/bin/sh", "-c"]
ENTRYPOINT poetry run python3 -m uvicorn main:app --app-dir src --host 0.0.0.0 --port $HTTP_PORT