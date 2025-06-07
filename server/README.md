# Setup guide for servers

## Naming conventions

- App data: `<CATEGORY>/<SERVICE>/<FOLDER>` E.g. `nextcloud/mariadb/data`

## Installation

### Debian

Download latest version from <https://www.debian.org/distrib/netinst>

### Rocky

1. Download latest version from <https://rockylinux.org/download>
2. Install with following settings:
   - Software selection = Minimal
   - Installation Destination = Automatic + Encrypt my data
   - KDUMP = Disabled
   - User Creation = Add non-root user

### VM clone

```bash
clone-vm <FROM> <TO>
```

### VPS / VM from ISO

```bash
# Login as root to VPS
# You might have to set "PermitRootLogin yes" in /etc/ssh/sshd_config and restart ssh(d) service
ssh root@...

# Rocky - Create personal admin user
PERS_USER=""
adduser --groups wheel --comment "" ${PERS_USER:?}
passwd ${PERS_USER:?}

# Debian - Create personal admin user
PERS_USER=""
adduser --comment "" ${PERS_USER:?}
apt-get install -y sudo
usermod -aG sudo ${PERS_USER:?}

# Impersonate new user (ensures sudo works correctly)
sudo -iu ${PERS_USER:?}

# Lock the root account
sudo passwd -l root
```

## Setup

Download the latest version of [Debian](https://www.debian.org/distrib/netinst)
or [Rocky](https://rockylinux.org/download) and install. Next, run following steps:

```bash
# Set authorized SSH keys
mkdir -p ~/.ssh
chmod 700 ~/.ssh
vi ~/.ssh/authorized_keys

# Rocky - Update system
sudo dnf upgrade -y

# Update system for Debian
sudo apt-get update
sudo apt-get dist-upgrade -y

# Reboot to enable latest kernel
sudo reboot
```

## Run playbook

As a failsafe, it's mandatory to use `--limit` option.
Without this option, the playbook will fail.

```bash
# Install Ansible and Python requirements
sudo apt install pipx
pipx install ansible-core
pipx inject ansible-core $(cat requirements.txt | sed 's/\n/ /g' | sed 's/#.*//') # pipx on Debian 12 is too old to support flag "-r"

# Install roles and collections
ansible-galaxy role install --force -r requirements.yml
ansible-galaxy collection install --force -r requirements.yml

# Run complete setup
ansible-playbook vm_host.yml
# OR
ansible-playbook docker_host.yml

# To only run Docker steps for a specific host
ansible-playbook docker_host.yml --tags docker --limit <HOSTNAME>
```

## Special purpose VM's

- Home Assistant: https://www.home-assistant.io/installation/alternative/

## Service specific configuration

See [instructions for configuring services](./docs/how-to/General%20-%20Setup%20services.md)
