# Dockerfile.das
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV FASTAPI_PORT=8000

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt .

# Install dependencies (only FastAPI and Uvicorn needed for this service)
RUN pip install --no-cache-dir fastapi uvicorn

# Copy application code
COPY das.py .
COPY test_das.py .

# Expose the application port
EXPOSE 8000

# Command to run the service using Uvicorn (a fast ASGI server)
CMD ["uvicorn", "das:app", "--host", "0.0.0.0", "--port", "8000"]
