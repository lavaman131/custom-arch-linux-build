#!/bin/bash

[[ "$1" == "up" ]] && pactl set-sink-volume @DEFAULT_SINK@ +5%
[[ "$1" == "down" ]] && pactl set-sink-volume @DEFAULT_SINK@ -5%
[[ "$1" == "mute" ]] && pactl set-sink-mute @DEFAULT_SINK@ toggle

# get volume
VOL=$(pactl list sinks | grep '^[[:space:]]Volume:' | \
    head -n $(( $SINK + 1 )) | tail -n 1 | sed -e 's,.* \([0-9][0-9]*\)%.*,\1,')

MUTE=$(pacmd list-sinks | awk '/muted/ { print $2 }' | head -1)


if [ "$MUTE" == "no" ]; then
    volnoti-show $VOL 
else
    volnoti-show -m $VOL 
fi