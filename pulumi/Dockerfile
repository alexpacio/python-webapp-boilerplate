FROM pulumi/pulumi-python:3.132.0

ARG TARGET

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    TARGET=${TARGET} \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR='/tmp/poetry_cache' \
    VENV_PATH="/app/venv"

# System deps:
RUN pip3 install poetry==1.8.3

# Copy only requirements to cache them in docker layer
WORKDIR /app
RUN mkdir venv
COPY poetry.lock pyproject.toml README.md /app/

# Project initialization:
RUN poetry install $(test "$TARGET" == production && echo "--only=main") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY infra /app/infra/

WORKDIR /app/infra

RUN rm -rf __pycache__ venv

RUN python3 -m venv venv
ENV PATH="venv/bin:$PATH"
RUN venv/bin/pip install -r requirements.txt

WORKDIR /app
SHELL ["/bin/sh", "-c"]
ENTRYPOINT poetry env use system && export AWS_ENDPOINT_URL="$LOCALSTACK_HOST" && poetry run pulumilocal refresh --stack $PULUMI_STACK_NAME --cwd infra --yes -f && poetry run pulumilocal up --stack $PULUMI_STACK_NAME --cwd infra --yes -f