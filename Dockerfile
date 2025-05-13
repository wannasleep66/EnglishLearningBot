FROM python:3.12-slim

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install --no-cache-dir poetry

RUN poetry install --no-root

COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]


ENV PYTHONPATH=/app
CMD ["poetry", "run", "python", "src/main.py"]


