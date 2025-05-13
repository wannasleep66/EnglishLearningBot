#!/bin/bash

echo "Applying migrations"

poetry run alembic upgrade head

echo "Running seeds"
poetry run python src/database/seeds/__init__.py

exec "$@"