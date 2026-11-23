# AI host

Eventually, all setup actions should be automated in Ansible.
However, documenting here allows to have quick iterations before full automation is implemented.

## General

Run the Ansible playbook using:

```bash
ansible-playbook ai_host.yml
```

## Hermes

### Install dependencies

#### UV

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

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

#### QMD

See https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/research/research-qmd

```bash
# Install NodeJS repo
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -

# Install NodeJS
sudo apt update
sudo apt-get install -y nodejs

# Install QMD
sudo npm install -g @tobilu/qmd

# Configure collections
qmd collection add ~/Data/agent-config --name agent-config --mask "**/*.md"
qmd context add qmd://agent-config "skills and configs related to the Hermes agent"
qmd collection add ~/Data/assets --name assets --mask "**/*.md,**/*.yml,**/*.yaml"
qmd context add qmd://assets "computers, components, household items and other assets"
qmd collection add ~/Data/silverbullet-space-main --name silverbullet-space-main --mask "**/*.md"
qmd context add qmd://silverbullet-space-main "main knowledge base"

# Generate embeddings
qmd embed
```

## Setup Hermes

```bash
# Install Hermes agent
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
# How would you like to set up Hermes? => Full setup
# Provider => Custom endpoint (enter URL manually)
# API base URL => https://api.mistral.ai/v1
# API key => See https://admin.mistral.ai/organization/api-keys
# Model => Enter (no input)
# Context length => Enter (no input)
# Display name => Mistral
# Select terminal backend => Local
# Select platforms to configure => Signal
# HTTP URL => http://127.0.0.1:8666
# Account number => Enter phone number
# Allowed account => Keep default (only own phone number)
# Enable group messaging => No
# Tools for CLI => Enter (no input)
# Choose a provider => Local Browser
# Choose a provider => Skip
# Choose a provider (TTS) => Mistral
# Vision backend => Auto
# Search provider => Brave Search
# Help improve Hermes? => No
# Start the gateway automatically on login/boot with systemd? => Yes

# Configure Hermes
hermes config set model.default mistral-small-latest
hermes config set model.provider custom:mistral
hermes config set model.base_url https://api.mistral.ai/v1

hermes config set providers.mistral.name Mistral
hermes config set providers.mistral.api https://api.mistral.ai/v1
hermes config set providers.mistral.key_env MISTRAL_API_KEY
hermes config set providers.mistral.discover_models "true"
hermes config set providers.mistral.default_model mistral-small-latest
hermes config set providers.mistral.models '["mistral-large-latest","mistral-medium-latest","mistral-small-latest","codestral-latest","devstral-medium-latest","devstral-latest","ministral-8b-latest","ministral-3b-latest"]'

hermes config set providers.hercules.name Hercules
hermes config set providers.hercules.api http://hercules.jensw.eu:8080/v1
hermes config set providers.hercules.discover_models "true"
hermes config set providers.hercules.models '[]'

# See https://hermes-agent.nousresearch.com/docs/user-guide/messaging/signal#manual-configuration
editor ~/.hermes/.env

# Restart the Hermes Gateway
hermes gateway restart --all
```
