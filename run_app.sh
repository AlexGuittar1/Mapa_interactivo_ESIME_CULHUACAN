#!/bin/bash

# Kill running processes on port 5001 (Flask) and 5173 (Vite)
echo "Cleaning up ports..."
lsof -ti:5001 | xargs kill -9 2>/dev/null
lsof -ti:5173 | xargs kill -9 2>/dev/null

# Function to kill processes on exit
cleanup() {
    echo "Stopping application..."
    # Kill process group to ensure children die
    kill -TERM -$$ 2>/dev/null
    exit
}

trap cleanup SIGINT

echo "---------------------------------------"
echo "   ESIME Map App - Starting..."
echo "---------------------------------------"

# Backend
echo "[1/2] Starting Backend (Flask) on port 5001..."
python3 app.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to be ready
echo "Waiting for backend..."
sleep 2
if ! ps -p $BACKEND_PID > /dev/null; then
    echo "Backend failed to start! Check backend.log:"
    cat backend.log
    exit 1
fi

# Frontend
echo "[2/2] Starting Frontend (Vite)..."
cd frontend
npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

echo "---------------------------------------"
echo "   App Running!"
echo "   Backend Logs: tail -f backend.log"
echo "   Frontend Logs: tail -f frontend/frontend.log"
echo "   Open: http://localhost:5173"
echo "---------------------------------------"

wait
