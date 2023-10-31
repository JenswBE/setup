# Debian

## Installation

At `Software selection`, uncheck all except `standard system utilities`.

```bash
sudo apt-get install --no-install-recommends --no-install-suggests gnome-core network-manager-gnome libproxy1-plugin-networkmanager
sudo nano /etc/network/interfaces # Drop everything from '# The primary network interface'
sudo apt install flatpak
systemctl reboot
```

## Setup

:warning: First execute general instructions at [main README](../README.md).

```bash
# Install base packages
BASE_PACKAGES=$(grep -vE '^#.*' <<EOF
# Base
eject

# Containers
distrobox
podman
podman-compose

# Fingerprint auth
fprintd
libpam-fprintd

# VM's
virt-manager
EOF
)
sudo apt install -y ${BASE_PACKAGES:?}

# Don't hash SSH hosts (allows completion in Bash)
sudo lineinfile /etc/ssh/ssh_config 'HashKnownHosts ' '    HashKnownHosts no'

# Ensure GRUB contains non-Linux OS'es
sudo lineinfile /etc/default/grub 'GRUB_DISABLE_OS_PROBER=' 'GRUB_DISABLE_OS_PROBER=false'
sudo update-grub
```
