#!/bin/bash

python3 manage.py makemigrations && python3 manage.py migrate

#execute command launching gunicorn
exec gunicorn --bind 0.0.0.0:${PORT} src.wsgi
