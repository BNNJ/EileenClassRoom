FROM python:3.11-slim

ARG APP_VERSION=dev
ENV APP_VERSION=$APP_VERSION
ENV API_VERSION=$APP_VERSION

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
