# Fedora Silverblue

## Setup

```bash
# Basic setup
sudo hostnamectl hostname REPLACE_ME
mkdir -p ~/.config/autostart

# Add Flathub
flatpak remote-add --if-not-exists flathub-unfiltered https://flathub.org/repo/flathub.flatpakrepo
flatpak update --appstream

# Update system
flatpak update
rpm-ostree upgrade

# Setup auto-update
sudo tee /etc/systemd/system/flatpak-automatic.service <<EOF
[Unit]
Description=flatpak Automatic Update
Documentation=man:flatpak(1)
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/bin/flatpak update -y

[Install]
WantedBy=multi-user.target
EOF
sudo tee /etc/systemd/system/flatpak-automatic.timer <<EOF
[Unit]
Description=flatpak Automatic Update Trigger
Documentation=man:flatpak(1)

[Timer]
OnBootSec=5m
OnCalendar=0/6:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF
sudo tee /etc/rpm-ostreed.conf <<EOF
# Entries in this file show the compile time defaults.
# You can change settings by editing this file.
# For option meanings, see rpm-ostreed.conf(5).

[Daemon]
AutomaticUpdatePolicy=stage
IdleExitTimeout=60
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now /etc/systemd/system/flatpak-automatic.timer
sudo systemctl enable --now rpm-ostreed-automatic.timer
sudo systemctl enable --now rpm-ostree-countme.timer

# Use Firefox from Flathub (more codecs)
sudo rpm-ostree override remove firefox-langpacks firefox
sudo flatpak install flathub-unfiltered org.mozilla.firefox

# Install other software
flatpak_install="flatpak install flathub-unfiltered --assumeyes --noninteractive --or-update"
sudo $flatpak_install org.keepassxc.KeePassXC org.libreoffice.LibreOffice org.gnome.SimpleScan
$flatpak_install --user com.nextcloud.desktopclient.nextcloud

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
# Add custom keyboard shortcut to "/var/home/skipr/Documents/AppImages/Flameshot.AppImage gui"

# Create distroboxes
UBUNTU_VERSION=22.04
FEDORA_VERSION=37
distrobox-create -Y -i public.ecr.aws/ubuntu/ubuntu:${UBUNTU_VERSION:?} -n ubuntu-toolbox-main
distrobox-create -Y -i registry.fedoraproject.org/fedora-toolbox:${FEDORA_VERSION:?} --name fedora-toolbox-main

# Setup GNOME
gnome-extensions enable appindicatorsupport@rgcjonas.gmail.com
dconf load / <<EOF
[org/gnome/desktop/interface]
clock-show-weekday=true
color-scheme='prefer-dark'
gtk-theme='Adwaita-dark'

[org/gnome/desktop/search-providers]
disabled=['org.gnome.Software.desktop', 'org.gnome.Terminal.desktop', 'org.gnome.Nautilus.desktop']
enabled=['org.gnome.Characters.desktop']

[org/gnome/desktop/wm/preferences]
focus-mode='sloppy'
num-workspaces=1

[org/gnome/mutter]
dynamic-workspaces=false

[org/gnome/nautilus/preferences]
default-folder-viewer='list-view'

[org/gnome/settings-daemon/plugins/media-keys]
custom-keybindings=['/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/', '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom1/', '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom2/', '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom3/']

[org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0]
binding='Print'
command='${HOME:?}/Documents/AppImages/Flameshot.AppImage gui'
name='Flameshot'

[org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom1]
binding='<Shift><Super>h'
command='gnome-terminal --tab --profile Host'
name='Terminal - Host'

[org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom2]
binding='<Shift><Super>f'
command='gnome-terminal --tab --profile Fedora'
name='Terminal - Fedora'

[org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom3]
binding='<Shift><Super>u'
command='gnome-terminal --tab --profile Ubuntu'
name='Terminal - Ubuntu'

[org/gnome/terminal/legacy/profiles:]
list=['b1dcc9dd-5262-4d8d-a863-c897e6d979b9', '118048ea-b428-4d03-8a20-8795d1f518f6', '300c5c5e-2d73-45c2-9dde-6cf0a32512a5']

[org/gnome/terminal/legacy/profiles:/:118048ea-b428-4d03-8a20-8795d1f518f6]
custom-command='/usr/bin/distrobox-enter fedora-toolbox-main'
preserve-working-directory='always'
title='Fedora'
title-mode='after'
use-custom-command=true
visible-name='Fedora'

[org/gnome/terminal/legacy/profiles:/:300c5c5e-2d73-45c2-9dde-6cf0a32512a5]
background-color='rgb(23,20,33)'
custom-command='/usr/bin/distrobox-enter ubuntu-toolbox-main'
foreground-color='rgb(255,155,52)'
preserve-working-directory='always'
title='Ubuntu'
title-mode='after'
use-custom-command=true
use-theme-colors=false
visible-name='Ubuntu'

[org/gnome/terminal/legacy/profiles:/:b1dcc9dd-5262-4d8d-a863-c897e6d979b9]
background-color='rgb(0,0,0)'
foreground-color='rgb(7,178,7)'
preserve-working-directory='safe'
title='Host'
title-mode='after'
use-theme-colors=false
visible-name='Host'

[org/gnome/tweaks]
show-extensions-notice=false
EOF

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

## References

- https://github.com/castrojo/ublue
- https://github.com/ublue-os/ubuntu
- https://castrojo.github.io/awesome-immutable/
