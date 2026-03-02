# ── Stage: runtime ────────────────────────────────────────────────────────────
FROM python:3.12-slim

# Keeps Python from buffering stdout/stderr (useful for logging)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

WORKDIR /app

# Install dependencies first (Docker layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Create the instance folder for SQLite
RUN mkdir -p instance

# Expose Flask default port
EXPOSE 5000

# Run DB migrations then start the app
CMD ["sh", "-c", "flask db upgrade && python app.py"]