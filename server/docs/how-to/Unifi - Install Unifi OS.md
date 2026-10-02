# Install Unifi OS

Based on https://help.ui.com/hc/en-us/articles/34210126298775-Self-Hosting-UniFi


1. Clone a new VM using `clone-vm fiona-base-13 fiona-unifi-13`
2. Edit the VM networking settings
   - Interface type: `Bridge to LAN`
   - Source: `br-11wifi`
   - MAC address: Update to known address (Optional)
3. Enable `Autostart` on the VM
4. Boot the VM

Login with SSH and run:

```bash
# Ensure system is up-to-date
sudo apt update && sudo apt dist-upgrade -y
sudo reboot

# Install dependencies
sudo apt install -y podman uidmap slirp4netns curl

# Install Unifi OS
# See https://ui.com/download for the download URL
UNIFI_OS_DIR="/opt/unifi-os-server"
UNIFI_OS_URL="https://fw-download.ubnt.com/data/unifi-os-server/5172-linux-x64-5.1.42-12e9e3cf-8f8b-4e54-928c-76b80a10c8a4.42-x64"
mkdir -p "$UNIFI_OS_DIR"
wget -O install "$UNIFI_OS_URL"
chmod 755 install
sudo ./install
```

1. Visit https://192.168.11.50:11443
2. At `Create a UI Account` select `Proceed Without a UI Account`
