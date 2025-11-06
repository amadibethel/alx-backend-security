# ----------------------------
# Base Image
# ----------------------------
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev netcat-traditional && \
    apt-get clean

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run database migrations and start server
CMD ["sh", "-c", "python manage.py migrate && gunicorn ip_tracking.wsgi:application --bind 0.0.0.0:$PORT"]
