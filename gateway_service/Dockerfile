# Stage 1: Builder
FROM python:3.10-slim AS builder

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directoryz    
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --target=/app/dependencies -r requirements.txt

# Copy the application files
COPY . .

# Stage 2: Final image
FROM python:3.10-slim

# Install only runtime dependencies
RUN apt-get update && apt-get install -y ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependencies and application files from the builder stage
COPY --from=builder /app/dependencies /usr/local/lib/python3.10/site-packages
COPY --from=builder /app /app

# Expose the application port
EXPOSE 8000

# Define the command to run the application
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]