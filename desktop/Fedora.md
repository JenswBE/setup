# Fedora 36

## Setup

```bash
# Configure bash
tee -a ~/.bashrc <<EOF
export HISTCONTROL='ignoreboth'
export PS1='[\u@\h \w]\$ '
EOF

# Set hostname
sudo hostnamectl hostname <HOSTNAME>

# Basic setup
mkdir -p ~/.config/autostart

# Install useful software
sudo dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install -y https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install -y \
chromium \
gnome-tweaks \
nextcloud-client \
python3-devel \
python3-pip \
syncthing \
vim \
vlc \
zsh-syntax-highlighting
sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# Start Syncthing
systemctl enable --user --now syncthing

# Install media codecs
sudo dnf install -y gstreamer1-plugins-{bad-\*,good-\*,base} gstreamer1-plugin-openh264 gstreamer1-libav --exclude=gstreamer1-plugins-bad-free-devel
sudo dnf install -y lame\* --exclude=lame-devel
sudo dnf group upgrade -y --with-optional Multimedia

# Install Visual Studio Code
# See https://code.visualstudio.com/docs/setup/linux#_rhel-fedora-and-centos-based-distributions
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'
dnf check-update
sudo dnf install code
```

## Silverblue

To be executed after section `Setup`.

```bash
sudo tee /etc/rpm-ostreed.conf <<EOF
# Entries in this file show the compile time defaults.
# You can change settings by editing this file.
# For option meanings, see rpm-ostreed.conf(5).

[Daemon]
AutomaticUpdatePolicy=stage
IdleExitTimeout=60
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now rpm-ostreed-automatic.timer
sudo systemctl enable --now rpm-ostree-countme.timer

# Use Firefox from Flathub (more codecs)
sudo rpm-ostree override remove firefox-langpacks firefox
sudo flatpak install flathub-unfiltered org.mozilla.firefox

# Overlay packages
sudo rpm-ostree --idempotent install gnome-shell-extension-appindicator gnome-tweaks distrobox
systemctl reboot

# Install Flameshot
mkdir -p   ~/Documents/AppImages
wget -O ~/Documents/AppImages/Flameshot.AppImage https://github.com/flameshot-org/flameshot/releases/download/v12.1.0/Flameshot-12.1.0.x86_64.AppImage
chmod 755 ~/Documents/AppImages/Flameshot.AppImage
cat > ~/.local/share/applications/flameshot-daemon.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Version=1.0
Type=Application
Terminal=false
Exec=${HOME:?}/Documents/AppImages/Flameshot.AppImage
Name=Flameshot Daemon
EOF
cp ~/.local/share/applications/flameshot-daemon.desktop ~/.config/autostart/

# Create distroboxes
UBUNTU_VERSION=22.04
FEDORA_VERSION=38
distrobox-create -Y -i public.ecr.aws/ubuntu/ubuntu:${UBUNTU_VERSION:?} -n ubuntu-toolbox-${UBUNTU_VERSION:?}
distrobox-create -Y -i registry.fedoraproject.org/fedora-toolbox:${FEDORA_VERSION:?} --name fedora-toolbox-${FEDORA_VERSION:?}

# Disable PipeWire HSP/HFP profile
# Since I use the build-in mic of my computer, I want to always use A2DP instead of HSP/HFP.
# Based on https://wiki.archlinux.org/title/bluetooth_headset#Disable_PipeWire_HSP/HFP_profile
sudo cp /usr/share/wireplumber/bluetooth.lua.d/50-bluez-config.lua /etc/wireplumber/bluetooth.lua.d/50-bluez-config.lua
# Update following properties:
#   - bluez_monitor.properties
#     ["bluez5.headset-roles"] = "[ ]",
#     ["bluez5.hfphsp-backend"] = "none",
#   - bluez_monitor.rules => apply_properties
#     ["bluez5.auto-connect"] = "[ a2dp_sink ]",
#     ["bluez5.hw-volume"] = "[ a2dp_sink ]",
nano /etc/wireplumber/bluetooth.lua.d/50-bluez-config.lua

# Setup Fedora distrobox
distrobox enter fedora-toolbox-main

# Setup VS Code
# See https://code.visualstudio.com/docs/setup/linux#_rhel-fedora-and-centos-based-distributions
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo tee /etc/yum.repos.d/vscode.repo <<EOF
[code]
name=Visual Studio Code
baseurl=https://packages.microsoft.com/yumrepos/vscode
enabled=1
gpgcheck=1
gpgkey=https://packages.microsoft.com/keys/microsoft.asc
EOF
dnf check-update
sudo dnf install code
distrobox-export --app code
```

### References

- https://github.com/castrojo/ublue
- https://github.com/ublue-os/ubuntu
- https://castrojo.github.io/awesome-immutable/
