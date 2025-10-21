#!/bin/bash
export DISPLAY=:0
export LIBGL_ALWAYS_SOFTWARE=1

# Wait for X to be ready
for i in {1..20}; do
    if xset q &>/dev/null; then
        break
    fi
    sleep 1
done

# Wait for symlink to exist and point to a real image (not splash)
for i in {1..20}; do
    if [ -L /home/pi/frame-app/static/current.jpg ]; then
        TARGET=$(readlink -f /home/pi/frame-app/static/current.jpg)
        if [[ "$TARGET" != "/usr/share/plymouth/themes/pix/splash.png" && -f "$TARGET" ]]; then
            break
        fi
    fi
    sleep 5
done

# Launch feh
/usr/bin/feh --fullscreen --hide-pointer --borderless --auto-zoom --reload 2 --geometry 3840x2160 /home/pi/frame-app/static/current.jpg &
