#!/bin/bash

set -o errexit
set -o nounset

celery -A task.worker.celery worker --loglevel=info
