# Ubuntu 20.04

## Install

COMPLETE_ME

## Setup

```bash
# Update OS
sudo apt update && sudo apt dist-upgrade -y

# Enable grapic drivers repo
sudo add-apt-repository ppa:graphics-drivers/ppa

# Install graphic drivers
sudo ubuntu-drivers install

# If using LVM: https://bugs.launchpad.net/ubuntu/+source/grub2/+bug/1273764
echo "GRUB_RECORDFAIL_TIMEOUT=5" >> /etc/default/grub
sudo update-grub

# Don't hash SSH hosts (allows completion in Bash)
sudo sed -i 's/HashKnownHosts yes/HashKnownHosts no' /etc/ssh/ssh_config

# Install basic software
# - hunspell/aspell/hyphen: Dutch spelling info for Libreoffice
# - gedit-plugin-draw-spaces: Gedit plugin to show whitespace characters
sudo apt install -y \
aspell-nl \
build-essential \
curl \
gedit-plugin-draw-spaces \
git \
gnome-tweaks \
hunspell-nl \
hyphen-nl \
nfs-common \
vim

# Config Git
git config --global user.name "Jens Willemsens"
git config --global user.email "...@users.noreply.github.com" # See https://github.com/settings/emails

# Configure Logitech HD Pro Webcam C920
# Based on https://wiki.archlinux.org/title/Webcam_setup
sudo tee /usr/bin/c920-config.sh <<EOF
#!/usr/bin/bash
/usr/bin/v4l2-ctl -d \$1 --set-ctrl=focus_auto=0,power_line_frequency=1,brightness=185
/usr/bin/v4l2-ctl -d \$1 --set-ctrl=focus_absolute=0 # Cannot work together with focus_auto=0
EOF
sudo chmod 755 /usr/bin/c920-config.sh
sudo tee /etc/udev/rules.d/99-logitech-c920-webcam.rules <<EOF
SUBSYSTEM=="video4linux", KERNEL=="video[0-9]*", ATTRS{idVendor}=="046d", ATTRS{idProduct}=="08e5", RUN+="/usr/bin/c920-config.sh \$devnode"
EOF

# Install Nextcloud
sudo add-apt-repository ppa:nextcloud-devs/client
sudo apt install nextcloud-client

# Install KeepassXC
sudo add-apt-repository ppa:phoerious/keepassxc
sudo apt install keepassxc ssh-askpass # For SSH agent confirmation

# Install eid
firefox 'https://eid.belgium.be/en/linux-eid-software-installation'
sudo dpkg -i ~/Downloads/eid-*
sudo apt-get update
sudo apt-get install eid-mw eid-viewer

# Install Brother MFC-L2710DW printer
firefox 'https://support.brother.com/g/b/downloadtop.aspx?c=us&lang=en&prod=mfcl2710dw_us_eu_as'
gunzip ~/Downloads/linux-brprinter-installer-*.gz
sudo bash ~/Downloads/linux-brprinter-installer-* MFC-L2710DW

# Install Syncthing
# Based on https://apt.syncthing.net/
sudo curl -s -o /usr/share/keyrings/syncthing-archive-keyring.gpg https://syncthing.net/release-key.gpg
echo "deb [signed-by=/usr/share/keyrings/syncthing-archive-keyring.gpg] https://apt.syncthing.net/ syncthing stable" | sudo tee /etc/apt/sources.list.d/syncthing.list
printf "Package: *\nPin: origin apt.syncthing.net\nPin-Priority: 990\n" | sudo tee /etc/apt/preferences.d/syncthing
sudo apt-get update
sudo apt-get install syncthing
# Launch app "Start Syncthing"
firefox 'http://localhost:8384'
```
