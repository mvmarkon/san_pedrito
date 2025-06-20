# Stage 1: Build dependencies
FROM python:3.11-slim-buster AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    musl-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Create the final image
FROM python:3.11-slim-buster

WORKDIR /app

# Install system dependencies for runtime (if any, e.g., libpq-dev for psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/

COPY . .

# Expose the port Django runs on
EXPOSE 8000

# Run Django migrations and start the server
CMD ["gunicorn", "san_pedrito.wsgi:application", "--bind", "0.0.0.0:8000"]