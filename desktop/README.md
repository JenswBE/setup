# Setup guide for desktops

Installation instructions for Hercules (Workstation) and Charmeleon (Laptop)

## Distro specific instructions

- [Debian](Debian.md)
- [Fedora](Fedora.md)

## Generic instructions

### Setup host

```bash
# Setup tools
sudo ln -fs "$(pwd)/lineinfile/lineinfile.py" /usr/local/bin/lineinfile

# Setup scripts
mkdir -p ~/.local/bin/
ln -fs "$(realpath ../scripts/bash/git-grep-all.sh)" ~/.local/bin/git-grep-all

# Configure bash
lineinfile ~/.bashrc 'export HISTSIZE=' 'export HISTSIZE=5000'
lineinfile ~/.bashrc 'export HISTFILESIZE=' 'export HISTFILESIZE=-1'

# Based on https://flathub.org/setup
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
sudo xargs flatpak install flathub --assumeyes --noninteractive --or-update <<EOF
org.gnome.SimpleScan
org.libreoffice.LibreOffice
org.videolan.VLC
EOF
xargs flatpak install --user flathub --assumeyes --noninteractive --or-update <<EOF
com.bitwarden.desktop
org.gimp.GIMP
org.gnome.gitlab.YaLTeR.VideoTrimmer
EOF

# Setup Flatpak auto-update
sudo tee /etc/systemd/system/flatpak-automatic.service > /dev/null <<EOF
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
sudo tee /etc/systemd/system/flatpak-automatic.timer > /dev/null <<EOF
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

# Setup NFS share
NFS_PATH=${HOME:?}/KuboMedia
NFS_SYSTEMD_NAME=$(systemd-escape --path ${NFS_PATH:?})
sudo tee /etc/systemd/system/${NFS_SYSTEMD_NAME:?}.mount > /dev/null <<EOF
[Unit]
Description=Mount Kubo Media
After=nss-lookup.target

[Mount]
What=kubo.jensw.eu:/data/media
Where=${NFS_PATH:?}
Options=noexec,nosuid,nofail,noatime,user
Type=nfs
TimeoutSec=5
ForceUnmount=true

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now ${NFS_SYSTEMD_NAME:?}.mount

# Setup Syncthing
mkdir -p ~/.config/syncthing
mkdir -p ~/Documents/Paperless
mkdir -p ~/Documents/Wiki.js
mkdir -p ~/Music/Syncthing
mkdir -p ~/.config/containers/systemd/
tee ~/.config/containers/systemd/syncthing.container > /dev/null <<EOF
[Unit]
Description=Syncthing
After=local-fs.target
After=network.target

[Container]
Image=docker.io/syncthing/syncthing:1
HostName=$(hostname)
Pull=always
Timezone=local
Volume=$(realpath ~/.config/syncthing):/var/syncthing:z
Volume=$(realpath ~/Documents/Paperless):/data/paperless:z
Volume=$(realpath ~/Documents/Wiki.js):/data/wikijs:z
Volume=$(realpath ~/Music/Syncthing):/data/music:z
PublishPort=127.0.0.1:8384:8384
PublishPort=22000:22000
Environment=TZ=$(timedatectl show | grep -F Timezone | cut -d'=' -f2)
UserNS=keep-id
Environment=PUID=$(id -u)
Environment=PGID=$(id -g)

[Install]
# Start by default on boot
WantedBy=multi-user.target default.target
EOF
systemctl --user daemon-reload

# Default to XOrg instead of Wayland
# Wayland doesn't work nicely with screensharing
sudo nano /etc/gdm/custom.conf # Add "DefaultSession=gnome-xorg.desktop" in section "daemon"
```

### GNOME

```bash
# Setup GNOME
dconf load / <<EOF
[org/gnome/desktop/interface]
clock-show-weekday=true
color-scheme='prefer-dark'
gtk-theme='Adwaita-dark'
show-battery-percentage=true

[org/gnome/desktop/privacy]
old-files-age=7
remove-old-trash-files=true

[org/gnome/desktop/search-providers]
disabled=['org.gnome.Software.desktop', 'org.gnome.Terminal.desktop', 'org.gnome.Nautilus.desktop', 'firefox.desktop']
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
custom-keybindings=['/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/', '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom1/', '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom2/']

[org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0]
binding='Print'
command='${HOME:?}/Documents/AppImages/Flameshot.sh'
name='Flameshot'

[org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom1]
binding='<Shift><Super>h'
command='gnome-terminal --tab --profile Host'
name='Terminal - Host'

[org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom2]
binding='<Shift><Super>f'
command='gnome-terminal --tab --profile Development'
name='Terminal - Development'

[org/gnome/shell/keybindings]
show-screenshot-ui=@as []

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
tee ~/Dev/Interwego/.gitconfig_include > /dev/null <<EOF
[user]
email = EMAIL
name = NAME
EOF
tee ~/.ssh/config > /dev/null <<EOF
Host github-personal
  HostName github.com
  User git
  IdentityFile ~/.ssh/personal
  IdentitiesOnly yes

Host github-interwego
  HostName github.com
  User git
  IdentityFile ~/.ssh/interwego
  IdentitiesOnly yes
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
${CMD_CODE_EXT_INSTALL:?} redhat.vscode-yaml
${CMD_CODE_EXT_INSTALL:?} vmsynkov.colonize

# Install latest LTS release of NodeJS
# following instructions at: https://github.com/nodesource/distributions

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
distrobox-export --app ICA

# Right click on .ica file and select "Open With ...".
# Use "Citrix Workspace Engine" and set as default.
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
