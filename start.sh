#!/bin/bash
# ── Shoppable AI Interior Designer ── Backend Startup ──

echo "🏠 Starting Shoppable AI Interior Designer Backend..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠  No .env file found. Copying from .env.example..."
    cp .env.example .env
    echo "📝 Please edit backend/.env and add your GEMINI_API_KEY before running."
fi

# Create virtual environment if needed
if [ ! -d "venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt -q

# Create necessary directories
mkdir -p uploads generated crops

# Load env vars
export $(grep -v '^#' .env | xargs) 2>/dev/null || true

# Start server
echo ""
echo "✅ Backend starting at http://localhost:8000"
echo "📖 API docs at http://localhost:8000/docs"
echo ""

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
