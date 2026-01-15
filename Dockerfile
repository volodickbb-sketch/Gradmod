FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app/ ./app/
COPY bot.py .
COPY dashboard.py .
COPY init_db.py .
COPY entrypoint.py .
COPY templates/ ./templates/
COPY alembic.ini .
COPY migrations/ ./migrations/

# Expose port for dashboard
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the bot (which also starts the dashboard)
CMD ["python", "entrypoint.py"]
