#!/bin/zsh

PORT=8080
PID=$(lsof -ti :$PORT 2>/dev/null)

if [ -n "$PID" ]; then
    echo "Stopping CodeArena (PID: $PID)..."
    kill -9 $PID 2>/dev/null
    echo "✅ CodeArena stopped."
else
    # Also check pkill by script name
    pkill -f "python3 server.py" 2>/dev/null
    echo "CodeArena is not running."
fi

