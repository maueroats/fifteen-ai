FROM mcr.microsoft.com/devcontainers/python:3.12

# 1. Install System Dependencies for GUI and VNC
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        xvfb \
        x11vnc \
        fluxbox \
        novnc \
        websockify \
        # Common dependencies for GUI apps (like Chrome/Firefox)
        libnss3 \
        libgbm1 \
        libasound2 
#    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 2. Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Setup noVNC workspace
# Link noVNC to the default location websockify expects
RUN ln -s /usr/share/novnc/vnc.html /usr/share/novnc/index.html

# 4. Environment variables for X11
ENV DISPLAY=:0
ENV RESOLUTION=1280x720x24

WORKDIR /workspaces/app

# We'll use a script to launch everything in order
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]