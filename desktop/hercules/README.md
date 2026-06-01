Based on https://gist.github.com/iamthenuggetman/6d0884954653940596d463a48b2f459c

# On local machine
scp files/* 192.168.20.124:

# On Bazzite

```bash
# Setup clevis/tang
sudo rpm-ostree kargs --append-if-missing="rd.neednet=1"
sudo rpm-ostree install clevis clevis-luks clevis-dracut
sudo rpm-ostree initramfs --enable

sudo reboot

# LUKS_DEVICE
# 1. Get UUID from /etc/crypttab
# 2. Value = /dev/disk/by-uuid/<UUID>
IP_FIONA=$(dig +short fiona.jensw.eu)
IP_KUBO=$(dig +short kubo.jensw.eu)
sudo clevis luks bind -d ${LUKS_DEVICE:?} sss "{\"t\":1,\"pins\":{\"tang\":[{\"url\":\"http://${IP_FIONA:?}:7500\"},{\"url\":\"http://${IP_KUBO:?}:7500\"}]}}"

sudo bash setup.sh

sudo rpm-ostree kargs --append-if-missing="firmware_class.path=/usr/local/lib/firmware drm.edid_firmware=DP-1:edid-dell-g2724d.bin video=DP-1:e"
```
