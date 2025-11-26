#!/bin/bash
# start.sh - start FastAPI with Gunicorn + Uvicorn workers
# make executable: chmod +x start.sh

gunicorn app.main:app -w ${GUNICORN_WORKERS:-4} -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
