# Setup guide for servers

## Naming conventions

- App data: `<CATEGORY>/<SERVICE>/<FOLDER>` E.g. `nextcloud/mariadb/data`

## Basic setup

Download the latest LTS version of [Ubuntu Server](https://ubuntu.com/download/server) and install. Next, run following steps:

```bash
# Set hostname
sudo hostnamectl set-hostname <HOSTNAME>

# Create new user
adduser <USERNAME>

# Add user to `sudo` group
adduser <USERNAME> sudo

# Login with new user
logout
ssh <USERNAME>@<FQDN>

# Disable root
sudo passwd -ld root

# Update system
sudo apt update
sudo apt dist-upgrade -y
sudo reboot

# Add SSH key on local machine
ssh-copy-id <USERNAME>@<FQDN>
```

## Run playbook

As a failsafe, it's mandatory to use `--limit` option.
Without this option, the playbook will fail.

```bash
# Install Python requirements
sudo pip install -r requirements.txt

# Install roles
LC_ALL=C.UTF-8 ansible-galaxy role install -r requirements.yml

# Run complete setup for a host
LC_ALL=C.UTF-8 ansible-playbook main.yml --limit <HOSTNAME>

# To only run Docker steps
LC_ALL=C.UTF-8 ansible-playbook main.yml --tags docker --limit <HOSTNAME>

# Available tags:
#   - setup
#   - config
#   - systemd
#   - docker
```

## Service specific configuration

See [instructions for configuring services](docs/how-to/Setup services.md)
