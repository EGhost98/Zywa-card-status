#!/bin/sh

until cd /app/backend
do
    echo "Waiting for server volume..."
done


until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

python manage.py collectstatic --noinput

# python manage.py merge_data // for merging data from csv to db 

DJANGO_SUPERUSER_PASSWORD=admin python manage.py createsuperuser --username=admin --email=admin@example.com --noinput

gunicorn core.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4

# for debug
# python manage.py runserver 0.0.0.0:8000