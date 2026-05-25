# Luffy - HA kiosk

1. Enable SSH
1. Enable passwordless sudo (needed for e.g. screen brightness)
   ```bash
    echo "${USER:?} ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/passwordless
    sudo chmod 440 /etc/sudoers.d/passwordless
   ```
1. Run `sudo raspi-config` and update the hostname to `luffy`
1. Install https://github.com/leukipp/touchkio
   ```bash
   wget -q https://raw.githubusercontent.com/leukipp/touchkio/main/install.sh

   # REVIEW!
   less install.sh

   # Install
   bash install.sh
   ```
