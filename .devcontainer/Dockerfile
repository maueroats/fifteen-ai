FROM mcr.microsoft.com/devcontainers/python:3

# 1. Install System Dependencies for GUI and VNC
RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        xvfb \
        x11vnc \
        fluxbox \
        novnc \
        websockify \
        supervisor \
        && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/log/supervisor
RUN mkdir -p /tmp/log

#libasound2 

# 2. Install uv (done byu features in devcontainer.json)
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# See features in devcontainer.json

# 3. Setup noVNC workspace
# Link noVNC to the default location websockify expects
RUN ln -s /usr/share/novnc/vnc.html /usr/share/novnc/index.html

# 4. Environment variables for X11
ENV DISPLAY=:0
ENV RESOLUTION=1280x720x24
ENV LOGDIR=/tmp/log

WORKDIR /workspaces/app

# We'll use a script to launch everything in order
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

COPY entrysupervisor /usr/local/bin/
RUN chmod +x /usr/local/bin/entrysupervisor

# ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
