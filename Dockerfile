FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.1.3

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock /app/


RUN poetry config virtualenvs.create false \
    && poetry install --no-root 

COPY ./src /app/src

COPY .env /app/

EXPOSE 8002

CMD ["uvicorn", "src.backend.main:app", "--host", "0.0.0.0", "--port", "8002"]

#docker build -t backend_auditoria .