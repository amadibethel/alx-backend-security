# =========================
# Stage 1: Base Image Setup
# =========================
FROM python:3.11-slim AS base

# Prevent Python from writing pyc files to disk and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create app directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port (Render will set $PORT automatically)
EXPOSE 8000

# =========================
# Stage 2: Command Logic
# =========================
# This logic allows one image to run both Django (web) and Celery (worker)
# based on the environment variable WORKER_MODE.
#
# If WORKER_MODE=true → run Celery worker
# else → run Gunicorn server for Django

CMD if [ "$WORKER_MODE" = "true" ]; then \
        echo "Starting Celery Worker..." && \
        celery -A ip_tracking worker --loglevel=info; \
    else \
        echo "Running Django Web Server..." && \
        python manage.py collectstatic --noinput && \
        python manage.py migrate && \
        gunicorn ip_tracking.wsgi:application --bind 0.0.0.0:${PORT:-8000}; \
    fi
