#!/bin/zsh

PORT=8080
PID=$(lsof -ti :$PORT)

if [ -n "$PID" ]; then
    echo "Stopping CodeArena (PID: $PID)..."
    kill -9 $PID
    echo "✅ CodeArena stopped."
else
    echo "CodeArena is not running."
fi

