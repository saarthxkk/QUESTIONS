#!/bin/zsh

PLIST="$HOME/Library/LaunchAgents/com.codearena.server.plist"
PYTHON="/usr/local/bin/python3"

if [ ! -f "$PYTHON" ]; then
    PYTHON=$(which python3)
fi

mkdir -p "$HOME/Library/LaunchAgents"

cat <<EOF > "$PLIST"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.codearena.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>$PYTHON</string>
        <string>/Users/saar.thxkk/Desktop/COMPILER/server.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/saar.thxkk/Desktop/COMPILER</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

launchctl unload "$PLIST" 2>/dev/null
launchctl load "$PLIST"

echo "✅ CodeArena Auto-Start Enabled!"
echo "The server will now automatically run silently in the background on your Mac."
echo "You can open http://localhost:8080 anytime!"

