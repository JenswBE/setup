# AI host

Eventually, all setup actions should be automated in Ansible.
However, documenting here allows to have quick iterations before full automation is implemented.

## Hermes

### Install dependencies

#### Signal-cli

```bash
# Install signal-cli
VERSION=$(curl -Ls -o /dev/null -w %{url_effective} https://github.com/AsamK/signal-cli/releases/latest | sed -e 's/^.*\/v//')
curl -L -O https://github.com/AsamK/signal-cli/releases/download/v"${VERSION}"/signal-cli-"${VERSION}"-Linux-native.tar.gz
sudo tar xf signal-cli-"${VERSION}"-Linux-native.tar.gz -C /opt
sudo ln -sf /opt/signal-cli /usr/local/bin/

# Link to Signal
signal-cli link -n HermesAgent

# Configure as daemon
PHONE_NUMBER="+1234567890" # Replace with your phone number associated with Signal
SIGNAL_CLI_PORT=8666
mkdir -p ${HOME:?}/.config/systemd/user
cat > ${HOME:?}/.config/systemd/user/signal-cli.service <<EOF
[Unit]
Description=signal-cli daemon
After=network.target

[Service]
ExecStart=signal-cli --account "${PHONE_NUMBER}" daemon --http 127.0.0.1:${SIGNAL_CLI_PORT}
Restart=always

[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now signal-cli
```

## Setup Hermes

```bash
# Install Hermes agent
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# Configure Hermes
# See https://hermes-agent.nousresearch.com/docs/user-guide/messaging/signal#manual-configuration
editor ~/.hermes/.env
cat >> ~/.hermes/.env <<'EOF'
# =============================================================================
# Nextcloud
# =============================================================================
NEXTCLOUD_USER=
NEXTCLOUD_APP_PASS=

# =============================================================================
# Silverbullet
# =============================================================================
SILVERBULLET_USER=
SILVERBULLET_PASS=
EOF

# Restart the Hermes Gateway
hermes gateway restart --all
```
