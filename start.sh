#!/bin/bash

# Startup script for NutriFit Agents API
set -e

echo "🚀 Starting NutriFit Agents API..."

# Wait for any dependencies (if needed)
echo "⏳ Initializing application..."

# Start the application with gunicorn
exec gunicorn \
    --bind 0.0.0.0:5000 \
    --workers 2 \
    --timeout 120 \
    --keep-alive 5 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --worker-class sync \
    --worker-tmp-dir /dev/shm \
    --capture-output \
    --enable-stdio-inheritance \
    --access-logfile - \
    --error-logfile - \
    --log-level debug \
    --pythonpath /app \
    main:app 
