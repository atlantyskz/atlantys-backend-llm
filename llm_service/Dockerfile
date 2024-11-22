# Stage 1: Builder
FROM python:3.10-slim AS builder

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --target=/app/dependencies -r requirements.txt

# Copy the application code
COPY . .

# Stage 2: Final image
FROM python:3.10-slim

WORKDIR /app

# Copy dependencies from the builder stage
COPY --from=builder /app/dependencies /usr/local/lib/python3.10/site-packages

# Copy application code from the builder stage
COPY --from=builder /app /app

# Expose the application port
EXPOSE 8001

# Define the command to run the application
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]