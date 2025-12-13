FROM python:3.12-slim

# Prevent Python from writing pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install minimal system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy everything needed for packaging
COPY pyproject.toml README.md ./
COPY app ./app
COPY ui ./ui

# Install project
RUN pip install --upgrade pip \
    && pip install .

# Expose FastAPI port
EXPOSE 8000

# Default entrypoint: FastAPI backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
