FROM python:3.12-slim

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install --no-cache-dir poetry

RUN poetry install --no-root

COPY . .

ENV PYTHONPATH=/app

CMD ["poetry", "run", "python", "src/main.py"]


