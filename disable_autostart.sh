#!/bin/zsh

PLIST="$HOME/Library/LaunchAgents/com.codearena.server.plist"

launchctl unload "$PLIST" 2>/dev/null
rm -f "$PLIST"

echo "✅ CodeArena Auto-Start Disabled."

