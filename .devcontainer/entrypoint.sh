#!/bin/bash
set -e

LOGDIR=/tmp/logs
mkdir $LOGDIR

# 1. Start Xvfb (Virtual Framebuffer)
nohup Xvfb $DISPLAY -screen 0 $RESOLUTION &> $LOGDIR/Xvfb.log &

# 2. Start Window Manager (Fluxbox) so windows have borders/controls
nohup fluxbox &> $LOGDIR/fluxbox.log &

# 3. Start VNC Server (No password for dev, mapped to display :0)
nohup x11vnc -display $DISPLAY  -ncache 10 -nopw -forever -quiet &> $LOGDIR/x11vnc.log &

# 4. Start noVNC bridge (Maps VNC to WebSockets for the browser)
nohup websockify --web /usr/share/novnc 6080 localhost:5900 &> $LOGDIR/websockify.log &

echo "Display ready! Access at http://localhost:6080"

# 5. Run the Python application using uv
# This ensures dependencies are synced before running
# uv sync
#exec uv run python main.py