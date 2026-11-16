#!/bin/zsh

# ─── CodeArena Quick Launcher ───
PORT=8080
DIR="/Users/saar.thxkk/Desktop/COMPILER"
PYTHON="/usr/local/bin/python3"

# Check if python3 exists at path, fallback to which python3
if [ ! -f "$PYTHON" ]; then
    PYTHON=$(which python3)
fi

cd "$DIR" || exit 1

# Check if server is already running on PORT
PID=$(lsof -ti :$PORT)

if [ -n "$PID" ]; then
    echo "⚡ CodeArena is already running (PID: $PID) at http://localhost:$PORT"
else
    echo "🚀 Starting CodeArena server..."
    nohup "$PYTHON" server.py > /dev/null 2>&1 &
    sleep 1
    echo "✅ CodeArena started successfully on http://localhost:$PORT"
fi

# Open browser
echo "🌐 Opening http://localhost:$PORT in your browser..."
open "http://localhost:$PORT"

