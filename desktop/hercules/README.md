# CachyOS

This machine is a hybrid AI workstation and remote gaming rig.

## Setup

```bash
# => Install CachyOS

# => Enable SSH
sudo systemctl enable --now sshd
sudo ufw disable # We don't need firewall on this machine
nano .ssh/authorized_keys # Set authorized keys

# => Install base tools
#    - localsend: Easily send files and snippets
#    - paru: AUR helper
#    - rocm-smi-lib: Requirement to print GPU stats in btop
sudo pacman -S --noconfirm --needed localsend paru rocm-smi-lib

# => Enable automatic login (required by Sunshine)
sudo mkdir -p /etc/plasmalogin.conf.d
sudo tee /etc/plasmalogin.conf.d/zzz-autologin.conf >/dev/null <<EOF
[Autologin]
User=$USER
Session=plasma
Relogin=false
EOF

# => Disable automatic suspension and screen lock
kwriteconfig6 --file powerdevilrc --group AC --group SuspendAndShutdown --key AutoSuspendAction 0 --type uint --notify # Disable
kwriteconfig6 --file powerdevilrc --group AC --group SuspendAndShutdown --key PowerButtonAction 8 --type uint --notify # Shutdown
kwriteconfig6 --file kscreenlockerrc --group Daemon --key Autolock false --type bool --notify

# => Create a clean install snapshot
# Based on https://wiki.cachyos.org/configuration/btrfs_snapshots/#snapper-cli
sudo snapper create --type single --description "Clean install" --userdata "important=yes"
sudo snapper list

# => Setup Clevis with Tang SSS
# Based on https://wiki.archlinux.org/title/Clevis
# Install dependencies
sudo pacman -S --noconfirm --needed clevis
paru mkinitcpio-systemd-extras
# Bind Clevis to Tang SSS
bash # ensure we're in Bash
fiona_ip=$(dig +short fiona.jensw.eu)
kubo_ip=$(dig +short kubo.jensw.eu)
clevis_cfg=$(printf '{"t":1,"pins":{"tang":[{"url":"http://%s:7500"},{"url":"http://%s:7500"}]}}' "$fiona_ip" "$kubo_ip")
echo "${clevis_cfg}"
sudo clevis luks bind -d /dev/nvme0n1p2 sss "${clevis_cfg}"
# Ensure interfaces get an IP using DHCP at boot
sudo tee /etc/systemd/network/20-initramfs-dhcp.network > /dev/null <<EOF
[Match]
Name=*

[Network]
DHCP=yes

[DHCPv4]
ClientIdentifier=mac
EOF
# Add the systemd Clevis hooks
sudo nano /etc/mkinitcpio.conf
# HOOKS=(... sd-network sd-clevis sd-encrypt ...)
# Regenerate the initramfs
sudo limine-mkinitcpio

# => Install gaming related packages
sudo pacman -S --noconfirm --needed cachyos-gaming-meta cachyos-gaming-applications

# => Setup remote gaming
# Based on https://github.com/TheBrigandier/cachyos-sunshine-virt-display
sudo pacman -S --noconfirm --needed krfb kscreen jq sunshine
ln -sf /usr/share/applications/dev.lizardbyte.app.Sunshine.kwin.desktop ~/.config/autostart/sunshine.desktop

# => Setup Docker
sudo pacman -S --noconfirm --needed docker docker-compose containerd
sudo usermod -aG docker $USER
sudo systemctl enable --now docker

# => Setup AI tools
# Install packages
# Warning: This is the CPU version of llama.cpp. We need the Vulkan version for GPU acceleration.
sudo pacman -S --noconfirm --needed llama-cpp nvtop ollama opencode
# Install Hugging Face CLI
curl -LsSf https://hf.co/cli/install.sh | bash
hf auth login # Use access token with preset "Read-Only"
# Download models
mkdir -p ~/AI/models
hf_dl() { hf download "$1" --local-dir ~/AI/models; }
hf_dl hf://JetBrains/Mellum2.1-12B-A2.5B-Thinking-GGUF/Mellum2.1-12B-A2.5B-Thinking-Q4_K_M.gguf
hf_dl hf://JetBrains/Mellum2.1-12B-A2.5B-Thinking-GGUF/Mellum2.1-12B-A2.5B-Thinking-Q6_K.gguf
hf_dl hf://ISTA-DASLab/Qwen3.8-27B-GSQ-RCO-GGUF/Qwen3.8-27B-GSQ-RCO-IQ3_XXS.gguf
hf_dl hf://ISTA-DASLab/Qwen3.8-27B-GSQ-RCO-GGUF/Qwen3.8-27B-GSQ-RCO-IQ3_S.gguf
hf_dl hf://unsloth/Qwen3.5-9B-GGUF/Qwen3.5-9B-UD-Q6_K_XL.gguf
hf_dl hf://google/gemma-4-26B-A4B-it-qat-q4_0-gguf/gemma-4-26B_q4_0-it.gguf
hf_dl hf://google/gemma-4-12B-it-qat-q4_0-gguf/gemma-4-12b-it-qat-q4_0.gguf
hf_dl hf://bartowski/NousResearch_Hermes-4-14B-GGUF/NousResearch_Hermes-4-14B-Q4_K_M.gguf
hf_dl hf://bartowski/NousResearch_Hermes-4-14B-GGUF/NousResearch_Hermes-4-14B-Q4_K_L.gguf
hf_dl hf://bartowski/NousResearch_Hermes-4-14B-GGUF/NousResearch_Hermes-4-14B-Q5_K_M.gguf
hf_dl hf://bartowski/NousResearch_Hermes-4-14B-GGUF/NousResearch_Hermes-4-14B-Q5_K_L.gguf
# Run example
llama-b11669/llama-server --host 0.0.0.0 --port 8080 --models-dir ~/AI/models --models-max 1 --metrics --slots --parallel 1 --n-gpu-layers all --ctx-size 262144 --context-shift --flash-attn on

### Hermes
# Install dependencies
VERSION=$(curl -Ls -o /dev/null -w %{url_effective} https://github.com/AsamK/signal-cli/releases/latest | sed -e 's/^.*\/v//')
curl -L -O https://github.com/AsamK/signal-cli/releases/download/v"${VERSION}"/signal-cli-"${VERSION}"-Linux-native.tar.gz
sudo tar xf signal-cli-"${VERSION}"-Linux-native.tar.gz -C /opt
sudo ln -sf /opt/signal-cli /usr/local/bin/
# Install Hermes agent
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
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

### Configure OpenCode

Note: This is to be executed on your development machine. This can be another machine than the AI inference server.

```bash
# Configure OpenCode
mkdir -p ~/.config/opencode
ip=$(dig +short hercules.jensw.eu | head -n1)
jq \
  --arg baseURL "http://${ip:?}:8080/v1" \
  --argjson models "$(curl -fsS http://${ip:?}:8080/v1/models)" \
  '.provider.hercules.options.baseURL = $baseURL | .provider.hercules.models += ( $models.data | map({key: .id, value: {name: .id}) | from_entries )' \
  > ~/.config/opencode/opencode.json <<'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "build": {
      "temperature": 0.2,
      "permission": {
        "doom_loop": "allow"
      }
    }
  },
  "compaction": {
    "auto": true,
    "prune": true,
    "reserved": 10000
  },
  "permission": "allow",
  "provider": {
    "hercules": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Hercules",
      "options": {
        "apiKey": "none"
      },
      "models": {
        "strata": {
          "name": "strata",
          "limit": {
            "context": 65536,
            "output": 16384
          }
        }
      }
    }
  }
}
EOF

# Install skills
git clone https://github.com/samber/cc-skills-golang.git ~/.agents/skills/cc-skills-golang # Golang

# Run Hermes
docker run -it --rm -v ~/.hermes:/opt/data docker.io/nousresearch/hermes-agent

docker run -it --rm -v ~/.hermes:/opt/data --name hermes -p 8642:8642 -p 9119:9119 -e HERMES_DASHBOARD=1 docker.io/nousresearch/hermes-agent gateway run
```
