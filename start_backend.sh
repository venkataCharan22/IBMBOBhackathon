#!/bin/bash

# 🚀 Bug2PR Backend Startup Script
# Automatically sets up and runs the FastAPI backend

set -e

echo "🚀 Starting Bug2PR Backend..."
echo ""

cd backend

# Create virtual environment on first run
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update requirements on first run or if requirements changed
if [ ! -f "venv/.requirements_installed" ] || [ requirements.txt -nt venv/.requirements_installed ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.requirements_installed
    echo "✅ Dependencies installed"
    echo ""
fi

# Check for .env file and warn about missing keys
if [ ! -f ".env" ]; then
    echo "⚠️  WARNING: .env file not found!"
    echo "   Copy .env.example to .env and add your API keys:"
    echo "   - GITHUB_TOKEN (required for PR creation)"
    echo "   - GOOGLE_API_KEY (optional, for Gemini)"
    echo "   - GROQ_API_KEY (optional, for Groq)"
    echo ""
    echo "   Run: cp .env.example .env"
    echo ""
else
    # Check for important missing keys
    missing_keys=()
    
    if ! grep -q "^GITHUB_TOKEN=.\+" .env 2>/dev/null; then
        missing_keys+=("GITHUB_TOKEN")
    fi
    
    if [ ${#missing_keys[@]} -gt 0 ]; then
        echo "⚠️  WARNING: Missing important environment variables:"
        for key in "${missing_keys[@]}"; do
            echo "   - $key"
        done
        echo ""
        echo "   Add them to your .env file for full functionality"
        echo ""
    fi
fi

# Start the backend server
echo "🎯 Starting FastAPI server on http://localhost:8001"
echo "📚 API docs available at http://localhost:8001/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

# Made with Bob
