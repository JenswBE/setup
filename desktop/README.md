# Setup guide for desktops

Installation instructions for Hercules (Workstation) and Charmeleon (Laptop)

## Dual boot installation

When installing both Windows and Linux on a clean disk:

1. Create following partitions
   1. EFI partition: 512MB
   2. Blank space: Preferred size of Windows install
   3. Dummy partition: Ensures Windows doesn't go beyond preferred size
2. Install Windows
3. Start Fedora Silverblue install
4. Switch to terminal and launch `gdisk`
5. Remove dummy partition
6. Create `ext4` partition for `/boot`
7. Switch back to installer and reload disks
8. Set mount points for `/boot` and `/boot/efi`
9. Create partition with preffered size and mount point `/`
10. Mark root partition as `Encrypted`

## Generic instructions

```bash
# Set hostname
sudo hostnamectl hostname <HOSTNAME>

# Install Ansible
pipx install ansible-core
pipx inject ansible-core $(cat requirements.txt | sed 's/\n/ /g' | sed 's/#.*//') # pipx on Debian is too old to support flag "-r"

# Install collections
ansible-galaxy collection install --force -r requirements.yml

# Run Ansible - Part 1
ansible-playbook 00-before-reboot.yml

# Reboot system
sudo reboot

# Run Ansible - Part 2
ansible-playbook 10-after-reboot.yml
```

### Setup host

```bash
# Setup NFS share
NFS_PATH=${HOME:?}/KuboMedia
NFS_SYSTEMD_NAME=$(systemd-escape --path ${NFS_PATH:?})
sudo tee /etc/systemd/system/${NFS_SYSTEMD_NAME:?}.mount > /dev/null <<EOF
[Unit]
Description=Mount Kubo Media
After=nss-lookup.target

[Mount]
What=kubo.jensw.eu:/media
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

# Default to XOrg instead of Wayland
# Wayland doesn't work nicely with screensharing
sudo nano /etc/gdm/custom.conf # Add "DefaultSession=gnome-xorg.desktop" in section "daemon"
```

### Nextcloud

To add a second account in Nextcloud:

1. Search and start application `Nextcloud Desktop`
2. Click on dropdown left top with username
3. Click `Add account`

### Development

```bash
# Setup distrobox
# See https://github.com/89luca89/distrobox/blob/main/docs/compatibility.md#containers-distros
distrobox-create -Y -i quay.io/toolbx-images/debian-toolbox:12 --name debian-development --additional-flags "--env LC_ALL=C.UTF-8"
distrobox-enter debian-development

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

## Setup

```bash
# Install Android tools
# Based on https://discussion.fedoraproject.org/t/how-to-use-adb-android-debugging-bridge-on-silverblue/2475
wget https://dl.google.com/android/repository/platform-tools-latest-linux.zip
unzip platform-tools-latest-linux.zip
sudo cp -v platform-tools/adb platform-tools/fastboot platform-tools/mke2fs* /usr/local/bin
rm -rf platform-tools*
sudo wget -O /etc/udev/rules.d/51-android.rules 'https://raw.githubusercontent.com/M0Rf30/android-udev-rules/main/51-android.rules'
sudo chmod a+r /etc/udev/rules.d/51-android.rules
sudo groupadd adbusers
sudo usermod -a -G adbusers $(whoami)
sudo systemctl restart systemd-udevd.service
adb kill-server
adb devices

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
```

### References

- https://github.com/castrojo/ublue
- https://github.com/ublue-os/ubuntu
- https://castrojo.github.io/awesome-immutable/
