# Setup guide for desktops

Installation instructions for Hercules (Workstation) and Charmeleon (Laptop)

## Install

[Dual-boot with Full Disk Encryption](Dual-boot%20with%20FDE.md)

## Distro specific instructions

- [Fedora 36](Fedora.md)
- [Ubuntu 20.04](Ubuntu.md)

## Generic instructions

```bash
# Configure git
git config --global user.name "<NAME>"
git config --global user.email "<EMAIL>"
```

### GNOME

- Appearance => Style => Select "Dark"
- Privacy => File History & Trash => Trash & Temporary Files => Enable "Automatically Delete Trash Content"
- Privacy => File History & Trash => Trash & Temporary Files => Automatically Delete Period => Set "7 days"
- Online Accounts => Nextcloud => Disable "Files"
- Sharing => Enable "Remote Login" (Only on fixed devices!)
- Displays => Night Light => Enable "Night Light"
- Region & Language => Your Account => Formats => Set to local format
- Region & Language => Login Screen => Formats => Set to local format

### GNOME Tweaks

- Appearance => Legacy Applications => Select "Adwaita-dark"
- Top Bar => Clock => Enable "Weekday"
- Top Bar => Calendar => Enable "Week Numbers"
- Windows => Window Focus => Select "Focus on Hover"

Startup applications:

- Nextcloud
- Syncthing
- KeepassXC

### VS Code

```bash
ln -fs "$(pwd)/vscode/settings.jsonc" ~/.config/Code/User/settings.json
ln -fs "$(pwd)/vscode/keybindings.jsonc" ~/.config/Code/User/keybindings.json
```

```
ext install esbenp.prettier-vscode
ext install golang.go
```

### Dracula

Install following files from Pro theme:

- Fonts
  - Cascadia Code
- Themes
  - VS Code

Install following files from non-Pro theme:

- [GNOME Terminal](https://draculatheme.com/gnome-terminal)

```bash
CUR_DIR=$(pwd)
cd ~/Documents/
git clone https://github.com/dracula/gnome-terminal
cd gnome-terminal
./install.sh # Interactive !!!
echo "eval \`dircolors ${HOME:?}/.dir_colors/dircolors\`" >> ~/.bashrc
cd ${CUR_DIR}
```

### Setup WakeOnLAN and SSH

1. Install required software with `sudo apt install -y ethtool openssh-server`
2. Copy `systemd/wol@.service` to `/etc/systemd/system/wol@.service`
3. Enable WOL with `sudo systemctl enable --now wol@<INTERFACE_NAME>.service`
4. Set fixed IP in Settings => Network => Wired - Edit => IPv4 to `192.168.20.50`
5. Use following DNS servers ([dns.watch](https://dns.watch)): `84.200.69.80` and `84.200.70.40`
6. Set hostname in Settings => Sharing => Computer Name
7. Create new group for SSH users with `sudo addgroup ssh-users`
8. Add preferred users to the group with `sudo adduser <USER> ssh-users`
9. Append following line to `/etc/ssh/sshd_config`:

```
AllowGroups ssh-users
```

10. Reboot

#### Arduino IDE

1. Get [Arduino IDE](https://www.arduino.cc/en/Main/Software)
2. Install pyserial with `python-serial` (required for esptool)
3. Add user to dialout group with `sudo usermod -a -G dialout <USERNAME>`
