#!/bin/bash

rotation="$(xrandr -q --verbose | grep 'connected' | egrep -o  '\) (normal|left|inverted|right) \(' | egrep -o '(normal|left|inverted|right)')"
stylus="Wacom ISDv4 E6 Pen stylus"
touch="Wacom ISDv4 E6 Finger touch"
eraser="Wacom ISDv4 E6 Pen eraser"



case "$rotation" in
    normal)
    # rotate 180
    xrandr -o inverted
    xsetwacom set "$stylus" rotate HALF
    xsetwacom set "$touch" rotate HALF
    xsetwacom set "$eraser" rotate HALF
    xsetwacom set "$touch" touch off
    xinput set-prop "$stylus" "Wacom Hover Click" 1
    ;;
    inverted)
    # rotate to normal
    xrandr -o normal
    xsetwacom set "$stylus" rotate none
    xsetwacom set "$touch" rotate none
    xsetwacom set "$eraser" rotate none
    xsetwacom set "$touch" touch on
    ;;
esac
