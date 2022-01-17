#!/bin/sh

lxsession &
xsetroot -cursor_name left_ptr &
picom --config ~/.config/picom/picom.conf --experimental-backends &
nitrogen --restore &
# nitrogen --set-scaled ~/wallpapers/$((1 + $RANDOM % $(ls -1 | wc -l))).jpg &
volnoti --timeout 2 &