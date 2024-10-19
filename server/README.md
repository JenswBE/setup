# Setup guide for servers

## Naming conventions

- App data: `<CATEGORY>/<SERVICE>/<FOLDER>` E.g. `nextcloud/mariadb/data`

## Basic setup

Download the latest version of [Debian](https://www.debian.org/distrib/netinst) and install. Next, run following steps:

```bash
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
# Install Ansible and Python requirements
sudo apt install pipx
pipx install ansible-core
pipx inject ansible-core $(cat requirements.txt | sed 's/\n/ /g' | sed 's/#.*//') # pipx on Debian is too old to support flag "-r"
sudo apt install -y dnsutils # Installs dig

# Install roles and collections
ansible-galaxy role install --force -r requirements.yml
ansible-galaxy collection install --force -r requirements.yml

# Run complete setup for a host
ansible-playbook main.yml --limit <HOSTNAME>

# To only run Docker steps
ansible-playbook main.yml --tags docker --limit <HOSTNAME>

# Available tags:
#   - setup
#   - config
#   - systemd
#   - docker
```

## Service specific configuration

See [instructions for configuring services](docs/how-to/Setup services.md)
