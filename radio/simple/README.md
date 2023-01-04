# Simple

## Installation

1. Download [latest DietPi](https://dietpi.com/)
2. Write image to USB stick using `dd if=<image> of=<device> bs=256k`
3. Connect with SSH to Raspberry Pi
4. Follow DietPi setup

## Setup

```bash
# Basic system setup
sudo apt update
sudo apt dist-upgrade -y

# Set hostname
sudo dietpi-config # => Security Options => Hostname

# Setup audio
sudo dietpi-config # => Audio Options => Enable => Sound card => rpi-bcm2835-3.5mm

# Install required software
sudo apt install -y wireguard snmpd ufw mplayer

# Configure UFW
sudo ufw allow 22
sudo ufw allow proto udp from 10.10.0.0/24 to any port 161
sudo ufw enable

# Configure snmpd
sudo nano /etc/snmp/snmpd.conf
# 1. Set "sysLocation"
# 2. Set "agentaddress" to "agentaddress :161" (All interfaces)
# 3. Add "rocommunity full default"
sudo systemctl enable --now snmpd

# Restart snmpd on failure
sudo mkdir -p /etc/systemd/system/snmpd.service.d
sudo tee /etc/systemd/system/snmpd.service.d/10-restart_on_failure.conf <<EOF
[Service]
Restart=on-failure
RestartSec=60s
EOF
sudo systemctl daemon-reload

# Configure Wireguard
# E.g. for remote SSH access without port forwarding
WG_CLIENT_PRIVATE_KEY="$(wg genkey)"
WG_CLIENT_PUBLIC_KEY="$(echo ${WG_CLIENT_PRIVATE_KEY} | wg pubkey)"
WG_SERVER_HOSTNAME="wireguard.jensw.be"
WG_SERVER_PUBLIC_KEY="fo/KW4qdas5WEuD4PDAkRyZIP2J2xNhFu/IO3BRKEWo="
WG_PRESHARED_KEY="$(wg genpsk)"
sudo tee /etc/wireguard/wg0.conf <<EOF
[Interface]
Address = 10.10.0.2/32
PrivateKey = ${WG_CLIENT_PRIVATE_KEY}

[Peer]
PublicKey = ${WG_SERVER_PUBLIC_KEY}
AllowedIPs = 10.10.0.1/32
Endpoint = ${WG_SERVER_HOSTNAME}:51820
PersistentKeepalive = 25
PresharedKey = ${WG_PRESHARED_KEY}
EOF
sudo chmod 600 /etc/wireguard/wg0.conf
sudo systemctl enable --now wg-quick@wg0

# Install Jingles service
sudo cp jingles.service /etc/systemd/system
sudo chown root:root /etc/systemd/system/jingles.service
sudo chmod 600 /etc/systemd/system/jingles.service
sudo systemctl daemon-reload
sudo systemctl enable --now jingles.service
```
