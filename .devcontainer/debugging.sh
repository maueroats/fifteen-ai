#!/bin/bash
echo "Debugging..."
date > debug.log

exec /usr/local/bin/entrypoint.sh
