FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install only what we need
RUN pip install --no-cache-dir Flask==3.0.3 mysql-connector-python==9.0.0

# Copy app
COPY app ./app

EXPOSE 8000
CMD ["python", "app/main.py"]
