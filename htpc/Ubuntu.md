# Ubuntu 20.04

## Install

- What apps would you like to install to start with: `Minimal installation`
- Enable `Install third-party software for graphics and Wi-Fi hardware and additional media formats`
- Set hostname to `rango` or `atom`
- Enable automatic login

## Setup

```bash
# Update system
sudo apt update && sudo apt dist-upgrade -y

# Install useful software
sudo apt install -y git vim openssh-server pavucontrol gnome-tweaks ubuntu-restricted-extras

# Install Nextcloud
sudo add-apt-repository ppa:nextcloud-devs/client
sudo apt install nextcloud-client

# Install KeepassXC
sudo add-apt-repository ppa:phoerious/keepassxc
sudo apt install keepassxc ssh-askpass # For SSH agent confirmation

# Install Chromium
sudo snap install chromium

# Clone this repo
git clone https://github.com/JenswBE/htpc.git ~/$HOSTNAME

# Setup "Swaps Caps Lock with Tab"
# Note: Doesn't work with Wayland!
cp ~/$HOSTNAME/fix-tab.desktop ~/.local/share/applications/

#
# Enable "Fix Tab" in Gnome Tweak Tool at startup
#

# Prevent audio buzzing
# https://unix.stackexchange.com/questions/565886/how-to-disable-the-power-saving-for-snd-hda-codec-realtek
sudo sed -i 's/^load-module module-suspend-on-idle/# load-module module-suspend-on-idle/' /etc/pulse/default.pa

# Install XanMod kernel to fix Intel UHD Graphics 605 display glitches
# Probably fix by kernel version bump from 3.13 to 3.15.
# See https://xanmod.org/
echo 'deb http://deb.xanmod.org releases main' | sudo tee /etc/apt/sources.list.d/xanmod-kernel.list
wget -qO - https://dl.xanmod.org/gpg.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/xanmod-kernel.gpg add -
sudo apt update && sudo apt install linux-xanmod
```
