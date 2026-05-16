#!/bin/bash

# 🎨 Bug2PR Frontend Startup Script
# Automatically sets up and runs the React frontend

set -e

echo "🎨 Starting Bug2PR Frontend..."
echo ""

cd frontend

# Install dependencies on first run or if package.json changed
if [ ! -d "node_modules" ] || [ package.json -nt node_modules/.install_timestamp ]; then
    echo "📦 Installing npm dependencies..."
    npm install
    touch node_modules/.install_timestamp
    echo "✅ Dependencies installed"
    echo ""
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "ℹ️  No .env file found, using defaults"
    echo "   (Optional) Copy .env.example to .env to customize"
    echo ""
fi

# Start the development server
echo "🎯 Starting Vite dev server on http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

npm run dev

# Made with Bob
