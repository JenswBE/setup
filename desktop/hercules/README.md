Based on https://gist.github.com/iamthenuggetman/6d0884954653940596d463a48b2f459c

# On local machine
scp files/* 192.168.20.124:

# On Bazzite
sudo bash setup.sh

sudo rpm-ostree kargs --append-if-missing="firmware_class.path=/usr/local/lib/firmware drm.edid_firmware=DP-1:edid-dell-g2724d.bin video=DP-1:e"
