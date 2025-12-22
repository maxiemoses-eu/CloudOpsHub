# Dockerfile.dis
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FASTAPI_PORT=8001

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt .

# Install dependencies (FastAPI + Uvicorn for serving)
RUN pip install --no-cache-dir fastapi uvicorn

# Copy application code
COPY dis.py .
COPY test_dis.py .

# Expose the application port
EXPOSE 8001

# Command to run the service using Uvicorn
CMD ["uvicorn", "dis:app", "--host", "0.0.0.0", "--port", "8001"]
