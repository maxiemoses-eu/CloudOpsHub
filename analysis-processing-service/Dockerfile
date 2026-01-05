# Stage 1: Build
FROM python:3.11-slim-bullseye AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Final
FROM python:3.11-slim-bullseye
RUN groupadd -r cloudop && useradd -r -g cloudop cloudop
WORKDIR /app

COPY --from=builder /root/.local /home/cloudop/.local
COPY . .

ENV PATH=/home/cloudop/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PORT=5000
RUN chown -R cloudop:cloudop /app

USER cloudop
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "aps:app"]