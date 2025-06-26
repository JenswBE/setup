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

## Setup

> [!IMPORTANT]
> - The pre-installed Firefox will be replaced with the flatpak version. So, no need to configure it yet.
> - When asked, don't enable Third Party repo's. Ansible will add the required Flathub repo's.

```bash
# Set hostname
sudo hostnamectl hostname <HOSTNAME>

# Install pipx
sudo rpm-ostree install pipx
sudo reboot

# Download repo
DEV_DIR=~/Dev/JenswBE # Keep in sync with vars.default_development_profile
SETUP_DIR=${DEV_DIR:?}/setup
mkdir -p ${DEV_DIR:?}
git clone https://github.com/JenswBE/setup.git ${SETUP_DIR:?}
cd ${SETUP_DIR:?}/desktop

# Install Ansible
pipx install --suffix='-host' ansible-core
pipx inject -r requirements.txt ansible-core-host

# Install collections
ansible-galaxy-host collection install --force -r requirements.yml

# Generate SSH key (configured by Ansible, but unable to create without interaction)
ssh-keygen -t ed25519-sk -O no-touch-required -f ~/.ssh/yubikey -C "Yubikey on ${HOSTNAME^}"

# Run Ansible - Part 1
ansible-playbook-host 00-before-reboot.yml

# Reboot system
sudo reboot

# Run Ansible - Part 2
ansible-playbook-host 10-after-reboot.yml

###################################
# BELOW STEPS RUN IN DISTROBOX!!! #
###################################

# Enter distrobox
distrobox-enter debian-development

# Install pipx and Ansible
sudo apt install -y pipx
pipx install ansible-core
pipx inject ansible-core $(cat requirements.txt | sed 's/\n/ /g' | sed 's/#.*//') # pipx on Debian 12 is too old to support flag "-r"
ansible-galaxy collection install --force -r requirements.yml

# Run playbook
ansible-playbook 20-setup-distrobox-development.yml

# Switch upstream URL of repo
git remote set-url origin git@github-jenswbe:JenswBE/setup.git

# Setup VS Code
# Based on https://code.visualstudio.com/docs/setup/linux.
wget -O code.deb CODE_PACKAGE_URL
sudo apt install ./code.deb
rm code.deb
distrobox-export --app code
# Start and stop VS Code (ensures below path is created)
ln -fs "$(pwd)/vscode/settings.jsonc" ~/.config/Code/User/settings.json
ln -fs "$(pwd)/vscode/keybindings.jsonc" ~/.config/Code/User/keybindings.json
CMD_CODE_EXT_INSTALL="code --force --install-extension"
${CMD_CODE_EXT_INSTALL:?} eamodio.gitlens
${CMD_CODE_EXT_INSTALL:?} golang.go
${CMD_CODE_EXT_INSTALL:?} HashiCorp.terraform
${CMD_CODE_EXT_INSTALL:?} redhat.ansible # Also installs "redhat.vscode-yaml" as dependency
${CMD_CODE_EXT_INSTALL:?} redhat.vscode-xml
${CMD_CODE_EXT_INSTALL:?} tintinweb.graphviz-interactive-preview

# Install latest LTS release of NodeJS
# following instructions at: https://github.com/nodesource/distributions

# Setup Go template support for Prettier
# Based on https://github.com/NiklasPor/prettier-plugin-go-template/issues/58#issuecomment-1085060511
sudo npm i -g prettier prettier-plugin-go-template
```

## Post-setup

### Syncthing

Visit <http://localhost:8384/> and connect hosts and folders.

### Nextcloud

To add a second account in Nextcloud:

1. Search and start application `Nextcloud Desktop`
2. Click on dropdown left top with username
3. Click `Add account`

## Disable PipeWire HSP/HFP profile

```bash
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

### Setup NFS mount

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
```

## Further docs

- [Android tools](./docs/android_tools.md)
- [Arduino IDE](./docs/arduino_ide.md)
- [Citrix](./docs/citrix.md)
- [Drivers](./docs/drivers.md)

## References

- https://github.com/castrojo/ublue
- https://github.com/ublue-os/ubuntu
- https://castrojo.github.io/awesome-immutable/
