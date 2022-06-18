# Fedora 36

Pro tip: Enable (and disable) VNC for generic instructions with

```bash
# Enable VNC
grdctl vnc enable
grdctl vnc set-password REPLACE_ME
grdctl vnc disable-view-only

# Disable VNC
grdctl vnc disable
```

## Setup

```bash
# Update system
sudo dnf update

# Install useful software
sudo dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install -y https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install -y chromium gnome-tweaks keepassxc kodi python3-devel python3-pip seahorse vim vlc
sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# Install media codecs
sudo dnf install -y gstreamer1-plugins-{bad-\*,good-\*,base} gstreamer1-plugin-openh264 gstreamer1-libav --exclude=gstreamer1-plugins-bad-free-devel
sudo dnf install -y lame\* --exclude=lame-devel
sudo dnf group upgrade -y --with-optional Multimedia

# Install Input Remapper
# See https://github.com/sezanzeb/input-remapper
sudo pip install evdev -U
sudo pip install --no-binary :all: git+https://github.com/sezanzeb/input-remapper.git
sudo systemctl enable input-remapper
sudo systemctl restart input-remapper
# Add following mappings:
#   - Caps Lock to Tab
#   - Menu button to Right mouse click

# Setup NFS share
sudo mkdir -p /kubo/media
sudo tee -a /etc/fstab <<< 'kubo.jensw.lan:/data/media /kubo/media nfs noexec,nosuid,nofail,noatime 0 0'
```

## Config

- Start Seahorse => Right click "Passwords.Login" => Change Password => Empty new password
