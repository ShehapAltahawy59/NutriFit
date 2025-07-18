#!/bin/bash

# Startup script for NutriFit Agents API (FastAPI/Uvicorn)
set -e

echo "🚀 Starting NutriFit Agents API..."

# Wait for any dependencies (if needed)
echo "⏳ Initializing application..."

# Start the application with Uvicorn (production)
exec uvicorn main:app \
    --host 0.0.0.0 \
    --port 8080 \
    --workers 2

# For development, you can use:
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
