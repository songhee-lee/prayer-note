#!/bin/bash

echo "Starting Prayer Note Backend Server (Development Mode)..."
echo "================================================"
echo "Server will run at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "================================================"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
