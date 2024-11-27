# Stage 1: Builder
FROM python:3.10-slim AS builder

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --target=/app/dependencies -r requirements.txt

COPY . .

# Stage 2: Final image
FROM python:3.10-slim

WORKDIR /app

# Copy dependencies and application files from the builder stage
COPY --from=builder /app/dependencies /usr/local/lib/python3.10/site-packages
COPY --from=builder /app /app


ENTRYPOINT [ "python","main.py" ]