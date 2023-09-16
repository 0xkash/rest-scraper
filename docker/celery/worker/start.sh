#!/bin/bash

set -o errexit
set -o nounset

celery -A task.worker.celery worker --loglevel=info --time-limit=300 --max-tasks-per-child=1