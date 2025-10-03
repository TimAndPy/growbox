# Multi-stage Dockerfile optimized for Nvidia Jetson Nano 2GB (ARM64)
# Base image: Python 3.8 on ARM64 (compatible with Jetson Nano)
FROM arm64v8/python:3.8-slim-bullseye

# Metadata
LABEL maintainer="GrowBox IoT"
LABEL description="GrowBox automated grow control system for Nvidia Jetson Nano"

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies needed for GPIO and sensors
# Keep this minimal to reduce image size for 2GB RAM constraint
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    python3-dev \
    build-essential \
    libgpiod2 \
    i2c-tools \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better layer caching)
COPY requirements.txt .

# Install Python dependencies
# Note: Jetson.GPIO may need special handling on actual Jetson hardware
# Install Adafruit-DHT from source for ARM64 compatibility
RUN pip install --no-cache-dir paho-mqtt==1.6.1 \
    Jetson.GPIO==2.1.6 \
    Flask==2.3.3 \
    Flask-SocketIO==5.3.4 \
    python-socketio==5.9.0 \
    smbus2==0.4.2 \
    pytest==7.4.2 \
    pytest-cov==4.1.0 \
    pytest-mock==3.11.1 \
    jsonschema==4.19.1 \
    python-dateutil==2.8.2

# Install Adafruit-DHT separately from source (better ARM64 support)
RUN pip install --no-cache-dir git+https://github.com/adafruit/Adafruit_Python_DHT.git

# Copy application code
COPY src/ ./src/
COPY config/ ./config/
COPY setup.py .
COPY pytest.ini .

# Create necessary directories
RUN mkdir -p /app/data /app/logs

# Expose Flask port
EXPOSE 5000

# Health check for container monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/status', timeout=5)" || exit 1

# Run the application
CMD ["python", "-m", "src.main"]
