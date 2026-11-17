#!/bin/bash

# ─── CodeArena Interactive Server Controller ───
PORT=8080
DIR="/Users/saar.thxkk/Desktop/COMPILER"
PYTHON="/usr/local/bin/python3"

if [ ! -f "$PYTHON" ]; then
    PYTHON=$(which python3)
fi

cd "$DIR" || exit 1

# Check current running status
PID=$(lsof -ti :$PORT 2>/dev/null)

echo ""
echo "============================================================"
echo "          🖥️   CodeArena Server Manager (Port $PORT)"
echo "============================================================"

if [ -n "$PID" ]; then
    echo "  Status:  🟢 ONLINE (PID: $PID)"
    echo "  URL:     http://localhost:$PORT"
    echo "============================================================"
    echo ""
    echo "Choose an action:"
    echo "  [1] Stop Server"
    echo "  [2] Open in Browser"
    echo "  [3] Restart Server"
    echo "  [4] Exit (keep server running)"
    echo ""
    printf "Enter choice [1/2/3/4] (Default is 1 to Stop): "
    read -r choice
    choice=${choice:-1}

    if [ "$choice" = "1" ]; then
        echo ""
        echo "🛑 Stopping CodeArena server (PID: $PID)..."
        kill -9 $PID 2>/dev/null
        pkill -f "python3 server.py" 2>/dev/null
        sleep 1
        echo "✅ CodeArena server has been STOPPED."
        echo ""
        printf "Press [Enter] to exit..."
        read -r dummy
        exit 0
    elif [ "$choice" = "2" ]; then
        echo "🌐 Opening http://localhost:$PORT in browser..."
        open "http://localhost:$PORT"
        exit 0
    elif [ "$choice" = "3" ]; then
        echo "🔄 Restarting server..."
        kill -9 $PID 2>/dev/null
        pkill -f "python3 server.py" 2>/dev/null
        sleep 1
        nohup "$PYTHON" server.py > /dev/null 2>&1 &
        sleep 1
        NEW_PID=$(lsof -ti :$PORT 2>/dev/null)
        echo "✅ Server restarted (PID: $NEW_PID) at http://localhost:$PORT"
        open "http://localhost:$PORT"
        echo ""
        printf "Press [Enter] to exit..."
        read -r dummy
        exit 0
    else
        echo "Leaving server running in background. Goodbye!"
        sleep 1
        exit 0
    fi
else
    echo "  Status:  🔴 STOPPED"
    echo "============================================================"
    echo ""
    echo "🚀 Starting CodeArena server..."
    nohup "$PYTHON" server.py > /dev/null 2>&1 &
    sleep 1

    NEW_PID=$(lsof -ti :$PORT 2>/dev/null)
    if [ -n "$NEW_PID" ]; then
        echo "✅ CodeArena started successfully (PID: $NEW_PID)!"
        echo "🌐 Server running at: http://localhost:$PORT"
        echo ""
        open "http://localhost:$PORT"
        echo "------------------------------------------------------------"
        echo "💡 The server is running in the background."
        echo "   Double-click this icon anytime to Stop or Restart."
        echo "   Or press [ENTER] right now to Stop it."
        echo "------------------------------------------------------------"
        echo ""
        printf "Press [ENTER] to STOP server now, or close window to keep running: "
        read -r action
        echo ""
        echo "🛑 Stopping CodeArena server (PID: $NEW_PID)..."
        kill -9 $NEW_PID 2>/dev/null
        pkill -f "python3 server.py" 2>/dev/null
        sleep 1
        echo "✅ CodeArena server has been STOPPED."
        sleep 1
        exit 0
    else
        echo "❌ Failed to start server. Check logs."
        printf "Press [Enter] to exit..."
        read -r dummy
        exit 1
    fi
fi
