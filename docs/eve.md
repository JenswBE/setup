# Eve
Hetzner VPS

## Setup
### Install Flatcar Container Linux
1. Boot into latest custom image of Arch Linux
```bash
# Set a new root password
passwd

# Start SSH server
systemctl start sshd
```

2. Connect with a local terminal
```bash
# Download latest flatcar-install
wget -O flatcar-install "https://raw.githubusercontent.com/flatcar-linux/init/flatcar-master/bin/flatcar-install"

# Download CoreOS Config Transpiler
wget -O ct "https://github.com/coreos/container-linux-config-transpiler/releases/download/v0.9.0/ct-v0.9.0-x86_64-unknown-linux-gnu"

# Make both files executable
chmod a+x ct flatcar-install

# Clone this repo
git clone git@github.com:JenswBE/eve.git

# Complete config
# Use `mkpasswd --method=SHA-512 --rounds=4096` to generate a secure password hash
vim eve/eve-clc.yml

# Transpile the config
./ct -strict < eve/eve-clc.yml > eve-clc.json

# Install Flatcar using
./flatcar-install -d /dev/sdX -C stable -i eve-clc.json

# Reboot server
reboot

```

### Configure SSH client

Append following lines to `~/.ssh/config`

```
Host eve
    HostName eve.jensw.be
    User jens
    IdentityFile ~/.ssh/eve
```

### Configure Flatcar
```bash
# Disable root and core user
sudo passwd -ld root
sudo passwd -ld core

# Change hostname
sudo hostnamectl set-hostname eve

# Set timezone
sudo timedatectl set-timezone Europe/Brussels

# Create opt folders
sudo mkdir -p /opt/{bin,conf,appdata}
```

### Docker Compose
Use [following instructions](https://docs.docker.com/compose/install/#install-compose) and install Docker compose at `/opt/bin/docker-compose-bin`

### Basic setup
1. Clone this repo with `git clone https://github.com/JenswBE/eve.git ~/eve; cd ~/eve`
2. Follow scripts in folder `setup/00-basics`

### Containers
#### Before up
1. Run `setup/01-before-up/borgmatic.sh`
1. Run `setup/01-before-up/delic.sh`
1. Run `setup/01-before-up/imap-alerter.sh`
1. Run `setup/01-before-up/isa.sh`
1. Run `setup/01-before-up/nextcloud.sh`
1. Run `setup/01-before-up/openvpn.sh`

#### After up
1. Run `setup/02-after-up/borgmatic.sh`
2. Run `setup/02-after-up/nextcloud.sh`
3. Run `setup/02-after-up/passit.sh`

## Scheduled jobs

### Continuous
- Every 5 mins: Nextcloud cron.php (/systemd/system/nextcloud-cron.timer)
- Every 10 mins: Nextcloud generate previews (/systemd/system/nextcloud-preview-generator.timer)

### 01:00 Daily application jobs
- Dead link checker (DeLiC): Check sites for dead links

### 02:00 Prepare backup
- Dump Nextcloud DB (/systemd/system/nextcloud-dump-db.timer)
- Dump Nextcloud calendars and contacts (/systemd/system/nextcloud-calcardbackup.timer)
- Dump Passit DB (/systemd/system/passit-dump-db.timer)

### 03:00 Perform backup
- Run Borgmatic (conf/borgmatic/borgmatic.d/crontab.txt)

### 04:00 Perform application updates
- 04:00 Run Watchtower (docker-compose.yml)
- 04:30 Update all Nextcloud apps (/systemd/system/nextcloud-update-apps.timer)

### System tasks
- 05:00 Update and restart (locksmith)
