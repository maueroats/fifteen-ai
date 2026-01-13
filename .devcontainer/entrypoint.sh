#!/bin/bash

# 1. Start Xvfb (Virtual Framebuffer)
Xvfb $DISPLAY -screen 0 $RESOLUTION &

# 2. Start Window Manager (Fluxbox) so windows have borders/controls
fluxbox &

# 3. Start VNC Server (No password for dev, mapped to display :0)
x11vnc -display $DISPLAY  -ncache 10 -nopw -forever -quiet &

# 4. Start noVNC bridge (Maps VNC to WebSockets for the browser)
websockify --web /usr/share/novnc 6080 localhost:5900 &

echo "Display ready! Access at http://localhost:6080"

# 5. Run the Python application using uv
# This ensures dependencies are synced before running
# uv sync
#exec uv run python main.py