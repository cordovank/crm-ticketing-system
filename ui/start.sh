#!/bin/sh
set -e

echo "Starting FastAPI backend..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

echo "Starting Gradio UI..."
python ui/app.py
