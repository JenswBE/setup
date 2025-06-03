# Setup guide for servers

## Naming conventions

- App data: `<CATEGORY>/<SERVICE>/<FOLDER>` E.g. `nextcloud/mariadb/data`

## User setup for VPS / VM

```bash
# Login as root to VPS
# You might have to set "PermitRootLogin yes" in /etc/ssh/sshd_config and restart ssh(d) service
ssh root@...

# Rocky - Create personal admin user
PERS_USER=""
adduser --groups wheel ${PERS_USER:?}
passwd ${PERS_USER:?}

# Debian - Create personal admin user
PERS_USER=""
adduser ${PERS_USER:?}
apt-get install -y sudo
usermod -aG sudo ${PERS_USER:?}

# Impersonate new user (ensures sudo works correctly)
sudo -iu ${PERS_USER:?}

# Setup SSH keys
mkdir -p ~/.ssh
chmod 700 ~/.ssh
editor ~/.ssh/authorized_keys

# Lock the root account
sudo passwd -l root
```

## Basic setup

Download the latest version of [Debian](https://www.debian.org/distrib/netinst)
or [Rocky](https://rockylinux.org/download) and install. Next, run following steps:

```bash
# Set authorized SSH keys
mkdir -p ~/.ssh
vi ~/.ssh/authorized_keys

# Update system for Debian
sudo apt-get update
sudo apt-get dist-upgrade -y

# Update system for Rocky
sudo dnf upgrade -y

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
ansible-playbook docker_host.yml

# To only run Docker steps for a specific host
ansible-playbook docker_host.yml --tags docker --limit <HOSTNAME>

# Available tags:
#   - setup
#   - config
#   - systemd
#   - docker
```

## Service specific configuration

See [instructions for configuring services](docs/how-to/Setup services.md)

## VM server

### Install Rocky

- Software selection = Minimal
- Installation Destination = Automatic + Encrypt my data
- KDUMP = Disabled
- User Creation = Add non-root user

### Post-install

1. Ensure system is up-to-date with `sudo dnf update`
2. Add authorized SSH keys
3. Run `ansible-playbook vm_host.yml -l HOSTNAME`
