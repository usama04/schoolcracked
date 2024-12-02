# Base image
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install dependencies
RUN apt-get update \
    && apt-get install -y gcc libpq-dev git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port 5001 for FastAPI
EXPOSE 5001

# Start the application
CMD ["python", "main.py"]