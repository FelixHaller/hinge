#!/bin/bash
rotation="$(xrandr -q --verbose | grep 'connected' | egrep -o  '\) (normal|left|inverted|right) \(' | egrep -o '(normal|left|inverted|right)')"

case "$rotation" in
    normal)
    # rotate 180
    xrandr -o inverted
    xsetwacom set "Wacom ISDv4 E6 Pen stylus" rotate HALF
    xsetwacom set "Wacom ISDv4 E6 Finger touch" rotate HALF
    xsetwacom set "Wacom ISDv4 E6 Pen eraser" rotate HALF
    xsetwacom set "Wacom ISDv4 E6 Finger touch" touch off
    ;;
    inverted)
    # rotate to normal
    xrandr -o normal
    xsetwacom set "Wacom ISDv4 E6 Pen stylus" rotate none
    xsetwacom set "Wacom ISDv4 E6 Finger touch" rotate none
    xsetwacom set "Wacom ISDv4 E6 Pen eraser" rotate none
    xsetwacom set "Wacom ISDv4 E6 Finger touch" touch on
    ;;
esac
