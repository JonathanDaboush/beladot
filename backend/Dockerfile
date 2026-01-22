FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies only if needed by future packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates bash \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first for better caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application (for production builds). In dev we will mount source.
COPY backend /app/backend
COPY alembic.ini /app/alembic.ini
COPY backend/db /app/backend/db

EXPOSE 8000

# Default to dev-friendly env
ENV ENV=dev

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
