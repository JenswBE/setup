# Fedora Silverblue

## Setup

```bash
# Configure bash
tee -a ~/.bashrc <<EOF
export HISTCONTROL='ignoreboth'
export PS1='[\u@\h \w]\$ '
EOF

# Set hostname
sudo hostnamectl hostname <HOSTNAME>

# Automatic system updates
sudo tee /etc/rpm-ostreed.conf <<EOF
# Entries in this file show the compile time defaults.
# You can change settings by editing this file.
# For option meanings, see rpm-ostreed.conf(5).

[Daemon]
AutomaticUpdatePolicy=stage
IdleExitTimeout=60
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now rpm-ostreed-automatic.timer
sudo systemctl enable --now rpm-ostree-countme.timer

# Use Firefox from Flathub (more codecs)
sudo rpm-ostree override remove firefox-langpacks firefox
sudo flatpak install --assumeyes --noninteractive flathub org.mozilla.firefox

# Overlay packages
sudo rpm-ostree --idempotent install distrobox gnome-tweaks nextcloud-client nextcloud-client-nautilus virt-manager libvirt
systemctl reboot

# Install Android tools
# Based on https://discussion.fedoraproject.org/t/how-to-use-adb-android-debugging-bridge-on-silverblue/2475
wget https://dl.google.com/android/repository/platform-tools-latest-linux.zip
unzip platform-tools-latest-linux.zip
sudo cp -v platform-tools/adb platform-tools/fastboot platform-tools/mke2fs* /usr/local/bin
rm -rf platform-tools*
sudo wget -O /etc/udev/rules.d/51-android.rules 'https://raw.githubusercontent.com/M0Rf30/android-udev-rules/main/51-android.rules'
sudo chmod a+r /etc/udev/rules.d/51-android.rules
sudo groupadd adbusers
sudo usermod -a -G adbusers $(whoami)
sudo systemctl restart systemd-udevd.service
adb kill-server
adb devices

# Install Flameshot
mkdir -p   ~/Documents/AppImages
wget -O ~/Documents/AppImages/Flameshot.AppImage https://github.com/flameshot-org/flameshot/releases/download/v12.1.0/Flameshot-12.1.0.x86_64.AppImage
chmod 755 ~/Documents/AppImages/Flameshot.AppImage
cat > ~/.local/share/applications/flameshot-daemon.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Version=1.0
Type=Application
Terminal=false
Exec=${HOME:?}/Documents/AppImages/Flameshot.AppImage
Name=Flameshot Daemon
EOF
mkdir -p ~/.config/autostart/
cp ~/.local/share/applications/flameshot-daemon.desktop ~/.config/autostart/
# Workaround for https://github.com/flameshot-org/flameshot/issues/3365
tee ~/Documents/AppImages/Flameshot.sh <<EOF
#!/usr/bin/bash
${HOME:?}/Documents/AppImages/Flameshot.AppImage gui
EOF
chmod 755 ~/Documents/AppImages/Flameshot.sh

# Disable PipeWire HSP/HFP profile
# Since I use the build-in mic of my computer, I want to always use A2DP instead of HSP/HFP.
# Based on https://wiki.archlinux.org/title/bluetooth_headset#Disable_PipeWire_HSP/HFP_profile
sudo cp /usr/share/wireplumber/bluetooth.lua.d/50-bluez-config.lua /etc/wireplumber/bluetooth.lua.d/50-bluez-config.lua
# Update following properties:
#   - bluez_monitor.properties
#     ["bluez5.headset-roles"] = "[ ]",
#     ["bluez5.hfphsp-backend"] = "none",
#   - bluez_monitor.rules => apply_properties
#     ["bluez5.auto-connect"] = "[ a2dp_sink ]",
#     ["bluez5.hw-volume"] = "[ a2dp_sink ]",
nano /etc/wireplumber/bluetooth.lua.d/50-bluez-config.lua
```

### References

- https://github.com/castrojo/ublue
- https://github.com/ublue-os/ubuntu
- https://castrojo.github.io/awesome-immutable/
