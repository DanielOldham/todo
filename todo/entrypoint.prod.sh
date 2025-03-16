#!/usr/bin/env bash
echo "$POSTGRES_PASSWORD" | psql --host dbprod --user postgres -W template1 -c "create role $DATABASE_USER with login password '$DATABASE_PASSWORD'"
echo "$POSTGRES_PASSWORD" | psql --host dbprod --user postgres -W template1 -c "create database $DATABASE_NAME with owner $DATABASE_USER"
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python -m gunicorn --bind 0.0.0.0:8000 --workers 3 todo.wsgi:application