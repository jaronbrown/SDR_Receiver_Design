#!/bin/bash

SDRGIT="/mnt/c/Users/beagl/sdrradio"
CONF="/config/quisk_conf_pico_pi.py"
CONF2=$CONF
ID=1000
GID=1000

sudo xhost +local:

if [ "$1" = "interactive" ]; then
    sudo docker run \
        -it \
        -e conf=$CONF \
        -e conf2=$CONF2 \
        -e DISPLAY=$DISPLAY \
        -e PULSE_SERVER=unix:/run/user/$ID/pulse/native \
        -v /run/user/$ID/pulse/native:/run/user/$ID/pulse/native \
        -v $SDRGIT/quisk/:/config/ \
        -v /tmp/.X11-unix/:/tmp/.X11-unix/ \
        --device /dev/ttyACM0:/dev/ttyACM0 \
        -u $ID:$GID \
        --group-add dialout quisk /bin/bash
else
    sudo docker run \
        -e conf=$CONF \
        -e conf2=$CONF2 \
        -e DISPLAY=$DISPLAY \
        -e PULSE_SERVER=unix:/run/user/$ID/pulse/native \
        -v /run/user/$ID/pulse/native:/run/user/$ID/pulse/native \
        -v $SDRGIT/quisk/:/config/ \
        -v /tmp/.X11-unix/:/tmp/.X11-unix/ \
        --device /dev/ttyACM0:/dev/ttyACM0 \
        -u $ID:$GID \
        --group-add dialout quisk
fi    
