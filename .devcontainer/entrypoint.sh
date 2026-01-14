#!/bin/bash -xv

set -e

echo "Beginning entrypoint script"


LOGDIR=/tmp/logs
mkdir $LOGDIR

mkdir -p ~/.vnc
chmod 700 ~/.vnc
x11vnc -storepasswd "${VNC_PASSWORD}" ~/.vnc/passwd

# 1. Start Xvfb (Virtual Framebuffer)
Xvfb $DISPLAY -screen 0 $RESOLUTION &> $LOGDIR/Xvfb.log &
sleep 1

# 2. Start Window Manager (Fluxbox) so windows have borders/controls
fluxbox &> $LOGDIR/fluxbox.log &
sleep 1

# 3. Start VNC Server 
x11vnc -display $DISPLAY  -ncache 10 -rfbauth ~/.vnc/passwd -forever -shared &> $LOGDIR/x11vnc.log &
sleep 1

# 4. Start noVNC bridge (Maps VNC to WebSockets for the browser)
websockify --web /usr/share/novnc 6080 localhost:5900 &> $LOGDIR/websockify.log &
sleep 1

echo "Display ready! Access at http://localhost:6080"

# 5. Run the Python application using uv
# This ensures dependencies are synced before running
# uv sync
#exec uv run python main.py
