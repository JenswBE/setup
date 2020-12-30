# Personal Ansible Stuff

## Conventions

## naming convention

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
# Run complete setup for a host
ansible-playbook main.yml --ask-vault-pass --ask-become-pass --limit <HOSTNAME>

# To only run config steps
ansible-playbook main.yml --ask-vault-pass --ask-become-pass --skip-tags setup --limit <HOSTNAME>

# To only run config Docker steps
ansible-playbook main.yml --ask-vault-pass --ask-become-pass --skip-tags setup,systemd --limit <HOSTNAME>
```

## Host specific configuration

- [Olaf](docs/olaf.md)
- [Eve](docs/eve.md)
