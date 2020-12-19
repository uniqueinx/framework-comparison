#!/usr/bin/env bash
/usr/local/bin/gunicorn -c /app/gunicorn_config.py  -b 0.0.0.0:5000 main:app --chdir=/app
