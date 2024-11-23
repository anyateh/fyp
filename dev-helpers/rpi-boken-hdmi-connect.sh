#!/use/bin/env sh

# cvt -v 1920 1080

# xrandr --newmode "1920x1080_60.00"  173.00  1920 2048 2248 2576  1080 1083 1088 1120 -hsync +vsync
xrandr --newmode $(cvt 1920 1080 | grep Modeline | awk '{$1=""}1' | awk '{$1=$1}1')
xrandr --addmode HDMI-1 "1920x1080_60.00"
xrandr --output HDMI-1 --mode 1920x1080_60.00
