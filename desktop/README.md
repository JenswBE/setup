# Desktop

Installation instructions for Hercules (Workstation) and Charmeleon (Laptop)

## Install

[Dual-boot with Full Disk Encryption](Dual-boot%20with%20FDE.md)

## Distro specific instructions

- [Fedora 36](Fedora.md)
- [Ubuntu 20.04](Ubuntu.md)

### Tweak Gnome

- Keyboard & Mouse => Additional Layout Options => Caps Lock behavior => Make Caps Lock additional backspace
- Top Bar => Activities Overview Hot Corner
- Top Bar => Weekday (in Clock)
- Top Bar => Weeknumbers (in Agenda)
- Windows => Focus on Hover
- Workspaces => Static Workspaces
- Workspaces => Number of Workspaces = 1

Startup applications:

- Nextcloud
- Syncthing
- KeepassXC

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
