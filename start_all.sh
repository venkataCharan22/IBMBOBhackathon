#!/bin/bash

# 🚀 Bug2PR Full Stack Startup Script
# Starts both backend and frontend with proper cleanup

set -e

echo "🚀 Starting Bug2PR Full Stack..."
echo "================================"
echo ""

# Trap Ctrl+C and cleanup
cleanup() {
    echo ""
    echo "🛑 Shutting down Bug2PR..."
    if [ ! -z "$BACKEND_PID" ]; then
        echo "   Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null || true
    fi
    echo "   Stopping frontend..."
    echo ""
    echo "✅ All services stopped"
    exit 0
}

trap cleanup INT TERM

# Start backend in background
echo "🔧 Starting backend server..."
./start_backend.sh > backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 3

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Backend failed to start. Check backend.log for details."
    exit 1
fi

echo "✅ Backend running on http://localhost:8001 (PID: $BACKEND_PID)"
echo "   Logs: tail -f backend.log"
echo ""

# Start frontend in foreground
echo "🎨 Starting frontend server..."
echo ""
./start_frontend.sh

# This line is reached when frontend exits
cleanup

# Made with Bob
