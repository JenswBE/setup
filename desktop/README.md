# Setup guide for desktops

Installation instructions for Hercules (Workstation) and Charmeleon (Laptop)

## Install

[Dual-boot with Full Disk Encryption](Dual-boot%20with%20FDE.md)

## Distro specific instructions

- [Debian](Debian.md)
- [Fedora](Fedora.md)

## Generic instructions

### Setup host

```bash
# Settings
CMD_PACKAGE_INSTALL="sudo apt install -y"

# Setup tools
sudo ln -fs "$(pwd)/lineinfile/lineinfile.py" /usr/local/bin/lineinfile

# Don't hash SSH hosts (allows completion in Bash)
sudo lineinfile /etc/ssh/ssh_config 'HashKnownHosts ' '    HashKnownHosts no'

# Install base packages
xargs ${CMD_PACKAGE_INSTALL:?} <<EOF
distrobox
eject
podman
podman-compose
virt-manager
EOF

# Configure bash
lineinfile ~/.bashrc 'export HISTSIZE=' 'export HISTSIZE=5000'
lineinfile ~/.bashrc 'export HISTFILESIZE=' 'export HISTFILESIZE=-1'

# Based on https://flathub.org/setup
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
sudo xargs flatpak install flathub --assumeyes --noninteractive --or-update <<EOF
com.bitwarden.desktop
org.gimp.GIMP
org.gnome.gitlab.YaLTeR.VideoTrimmer
org.gnome.SimpleScan
org.libreoffice.LibreOffice
org.mozilla.firefox
org.videolan.VLC
EOF

# Setup Flatpak auto-update
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
sudo systemctl daemon-reload
sudo systemctl enable --now flatpak-automatic.timer
```

### GNOME

```bash
# Setup GNOME
dconf load / <<EOF
[org/gnome/desktop/interface]
clock-show-weekday=true
color-scheme='prefer-dark'
gtk-theme='Adwaita-dark'

[org/gnome/desktop/privacy]
old-files-age=7
remove-old-trash-files=true

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

[org/gnome/settings-daemon/plugins/color]
night-light-enabled=true

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
command='gnome-terminal --tab --profile Development'
name='Terminal - Development'

[org/gnome/terminal/legacy/profiles:]
list=['b1dcc9dd-5262-4d8d-a863-c897e6d979b9', '118048ea-b428-4d03-8a20-8795d1f518f6']

[org/gnome/terminal/legacy/profiles:/:118048ea-b428-4d03-8a20-8795d1f518f6]
custom-command='/usr/bin/distrobox-enter debian-development'
preserve-working-directory='always'
title='Development'
title-mode='after'
use-custom-command=true
visible-name='Development'

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

[org/gtk/gtk4/settings/file-chooser]
sort-directories-first=true
EOF
```

### Development

```bash
# Setup distrobox
# See https://github.com/89luca89/distrobox/blob/main/docs/compatibility.md#containers-distros
distrobox-create -Y -i quay.io/toolbx-images/debian-toolbox:12 --name debian-development
distrobox-enter debian-development

# Setup development dirs
mkdir -p ~/Dev/{Personal,Interwego}

# Configure git
git config --global user.name "<NAME>"
git config --global user.email "<EMAIL>"
git config --global pull.ff only
tee ~/Dev/Interwego/.gitconfig_include <<EOF
[user]
email = EMAIL
name = NAME
EOF

# Setup VS Code
# Based on https://code.visualstudio.com/docs/setup/linux.
wget -O code.deb CODE_PACKAGE_URL
sudo apt install ./code.deb
rm code.deb
distrobox-export --app code
ln -fs "$(pwd)/vscode/settings.jsonc" ~/.config/Code/User/settings.json
ln -fs "$(pwd)/vscode/keybindings.jsonc" ~/.config/Code/User/keybindings.json
CMD_CODE_EXT_INSTALL="code --force --install-extension"
${CMD_CODE_EXT_INSTALL:?} eamodio.gitlens
${CMD_CODE_EXT_INSTALL:?} esbenp.prettier-vscode
${CMD_CODE_EXT_INSTALL:?} golang.go
${CMD_CODE_EXT_INSTALL:?} jinliming2.vscode-go-template

# Setup Go template support for Prettier
# Based on https://github.com/NiklasPor/prettier-plugin-go-template/issues/58#issuecomment-1085060511
sudo npm i -g prettier prettier-plugin-go-template
```

### Citrix

```bash
# Setup distrobox
# See https://github.com/89luca89/distrobox/blob/main/docs/compatibility.md#containers-distros
distrobox-create -Y -i quay.io/toolbx-images/debian-toolbox:12 --name debian-citrix
distrobox-enter debian-citrix

# Download latest Citrix Workspace app
# See https://www.citrix.com/downloads/workspace-app/linux/workspace-app-for-linux-latest.html
wget -O citrix.deb DOWNLOAD_URL
sudo apt install ./citrix.deb
distrobox-export --app receiver
distrobox-export --app ICA # Not sure this is required
```

### Drivers

#### rtl8811au

```bash
# Install rtl8811au drivers
# Based on:
#   - https://docs.alfa.com.tw/Support/Linux/RTL8811AU/
#   - https://github.com/aircrack-ng/rtl8812au
git clone -b v5.6.4.2 https://github.com/aircrack-ng/rtl8812au.git
cd rtl*
sudo dnf update # Important as "dkms" might install a newer kernel, but not modules for e.g. existing wireless devices.
sudo dnf install dkms
sudo make dkms_install
```

### Setup WakeOnLAN and SSH

```bash
# Install required software
sudo apt install -y ethtool openssh-server

# Copy config
sudo cp systemd/wol@.service /etc/systemd/system/wol@.service

# Enable service
sudo systemctl enable --now wol@<INTERFACE_NAME>.service

# Set static IP config
# Settings => Network => Wired - Edit

# Configure SSH users
sudo addgroup ssh-users
sudo adduser <USER> ssh-users
sudo tee -a /etc/ssh/sshd_config <<< "AllowGroups ssh-users"

# Reboot
systemctl reboot
```

### Arduino IDE

```bash
# Get Arduino IDE from https://www.arduino.cc/en/Main/Software

# Install pyserial (required for esptool)
sudo apt install python-serial

# Add user to dialout group
sudo usermod -a -G dialout <USERNAME>
```
