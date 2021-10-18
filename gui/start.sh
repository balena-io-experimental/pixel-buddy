#!/bin/bash 

# Wait for the x11 socket to appear in the shared volume
while [ ! -e /tmp/.X11-unix/X${DISPLAY#*:} ]; do sleep 0.1; done

python hello.py
