FROM python:3.11-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=aps.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt .

# Install dependencies (Flask)
RUN pip install --no-cache-dir flask

# Copy application code
COPY aps.py .
COPY test_aps.py .

# Expose the application port
EXPOSE 5001

# Command to run the service using Flask
CMD ["flask", "run"]
