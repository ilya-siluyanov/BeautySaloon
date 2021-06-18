# where is gunicorn package (installed via pip)?
command = '/app/venv/bin/gunicorn'
# what is the path to package with settings.py,etc. of the project?
pythonpath = '/app/src'
# which host and port to use?
bind = '127.0.0.1:8000'
# workers = 2 * available cores + 1
workers = 9
# username
user = 'entrant'
limit_request_fields = 32000
limit_request_field_size = 0
# environment variables
raw_env = ['DJANGO_SETTINGS_MODULE=src.settings']