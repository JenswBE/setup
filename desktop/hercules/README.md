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
sudo pacman -S --noconfirm --needed paru

# => Disable automatic suspension and screen lock
kwriteconfig6 --file powerdevilrc --group AC --group SuspendAndShutdown --key AutoSuspendAction 0 --type uint --notify
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
WAYLAND_DISPLAY=wayland-0 sunshine
# Connect to Sunshine using SSH port forwarding -> Configuration -> Advanced -> Force a Specific Capture Method = KWin Screencast

# => Setup AI tools
# Install packages
# Warning: This is the CPU version of llama.cpp. We need the Vulkan version for GPU acceleration.
sudo pacman -S --noconfirm --needed llama-cpp nvtop ollama opencode
# Install Hugging Face CLI
curl -LsSf https://hf.co/cli/install.sh | bash
hf auth login # Use access token with preset "Read-Only"
# Download models
mkdir -p ~/AI/models
hf download JetBrains/Mellum2.1-12B-A2.5B-Thinking-GGUF Mellum2.1-12B-A2.5B-Thinking-Q4_K_M.gguf --local-dir ~/AI/models
hf download JetBrains/Mellum2.1-12B-A2.5B-Thinking-GGUF Mellum2.1-12B-A2.5B-Thinking-Q6_K.gguf --local-dir ~/AI/models
hf download ISTA-DASLab/Qwen3.8-27B-GSQ-RCO-GGUF Qwen3.8-27B-GSQ-RCO-IQ3_XXS.gguf --local-dir ~/AI/models
hf download ISTA-DASLab/Qwen3.8-27B-GSQ-RCO-GGUF Qwen3.8-27B-GSQ-RCO-IQ3_S.gguf --local-dir ~/AI/models
# Run example
llama-server --host 0.0.0.0 --port 8080 --models-dir ~/AI/models --models-max 1 --metrics --slots --n-gpu-layers all
# Configure OpenCode
mkdir -p ~/.config/opencode
cat > ~/.config/opencode/opencode.json <<EOF
{
  "\$schema": "https://opencode.ai/config.json",
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
        "apiKey": "none",
        "baseURL": "http://$(dig +short hercules.jensw.eu):8080/v1"
      },
      "models": {
        "strata": {
          "name": "strata",
          "limit": {
            "context": 65536,
            "output": 16384
          }
        },
        "Mellum2.1-12B-A2.5B-Thinking-Q6_K": {
          "name": "Mellum2.1-12B-A2.5B-Thinking-Q6_K"
        }
      }
    }
  }
}
EOF
```
