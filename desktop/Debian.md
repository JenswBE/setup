# Debian

## Installation

At `Software selection`, uncheck all except `standard system utilities`.

# Setup

```bash
sudo apt-get install --no-install-recommends --no-install-suggests gnome-core network-manager-gnome libproxy1-plugin-networkmanager
sudo nano /etc/network/interfaces # Drop everything from '# The primary network interface'
sudo apt install flatpak
systemctl reboot
```
