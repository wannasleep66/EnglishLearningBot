#!/bin/bash


echo "Waiting for database"
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is up"

echo "Applying migrations"
alembic upgrade head

echo "Running seeds"
python app/seed.py

exec "$@"