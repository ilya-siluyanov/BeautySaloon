#!/bin/bash
#activate virtual environment
source /app/venv/bin/activate
#execute command launching gunicorn
exec gunicorn -c "/app/src/gunicorn_config.py" src.wsgi