#! /usr/bin/env bash
set -e

# python /app/app/celeryworker_pre_start.py

celery -A src.worker worker --beat -l info -E -Q "${STACK_NAME}"-queue --concurrency=1
