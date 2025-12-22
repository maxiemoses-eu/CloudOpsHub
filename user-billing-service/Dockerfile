# Dockerfile.ubs
FROM python:3.11-slim

# Set environment variables for the application
ENV FLASK_APP=ubs.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Set working directory inside the container
WORKDIR /app

# Copy dependency files
COPY requirements.txt .

# Install dependencies
# We use psycopg2-binary for PostgreSQL connectivity
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ubs.py .
COPY test_ubs.py .

# Expose the application port
EXPOSE 5000

# Command to run the service
CMD ["flask", "run"]
