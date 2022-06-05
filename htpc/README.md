# Setup guide for HTPC's

## Distro specific instructions

- [Fedora 36](Fedora.md)
- [Ubuntu 20.04](Ubuntu.md)

## Setup

### Shortcuts

- Firefox
- Chromium
- File manager
- Kodi
- KeepassXC
- Terminal

### System settings (GNOME 42)

- Appearance => Set "Dark" style
- Notifications => Enable "Do Not Disturb"
- Multitasking => Hot Corner => Disable
- Multitasking => Workspaces => Select "Fixed number of workspaces"
- Multitasking => Workspaces => Set "Number of Workspaces " to 1
- Online accounts => Add Nextcloud account (for KeepassXC access)
- Privacy => Location Services => Disable
- Privacy => Camera => Disable
- Privacy => Microphone => Disable
- Privacy => Screen Lock => Blank Screen Delay => Set to "never"
- Privacy => Screen Lock => Disable "Automatic Screen Lock"
- Power => Power Button Behavior => Set to "Power Off"
- Users => Enable "Automatic Login" on main user

### Firefox

1. General

- Restore previous session
- Always check if Firefox is your default browser

2. Home

- Home content: Disable Top Sites and Highlights

3. Search

- Delete all search engines but DuckDuckGo

4. Privacy & Security

- Disable `Ask to save logins and passwords for websites`

### KeepassXC

- View => Theme => Dark

### Plex Media Player

#### Install

```bash
wget -O ~/Documents/PMP.AppImage https://knapsu.eu/data/plex/latest
chmod a+x ~/Documents/PMP.AppImage
```

Next, double click the file

#### Auto start on boot

1. Start Gnome Tweak Tool
2. Startup applications => Add => Plex Media Player

#### Settings

1. Main
   - Automatically Sign In = Enabled
   - Language = English
   - Clock = 24 hour format
2. Video
   - Remote quality = Original
   - Hardware Decoding = Enabled
3. Audio
   - Device Type = HDMI
   - Channels = 5.1
4. Subtitles
   - Size = Large
5. Manual Servers
   - Connection 1 IP = <SERVER IP>

### Force HDMI audio on boot

1. Copy `hdmi.desktop` to `~/.local/share/applications/`
2. Start Gnome Tweak Tool
3. Startup applications => Add => Geluid HDMI surround

### Hyperion

#### HTPC

```bash
# Install Hyperion
# See https://docs.hyperion-project.org/en/user/Installation.html#supported-browsers
wget -qO- https://apt.hyperion-project.org/hyperion.pub.key | sudo gpg --dearmor -o /usr/share/keyrings/hyperion.pub.gpg
echo "deb [signed-by=/usr/share/keyrings/hyperion.pub.gpg] https://apt.hyperion-project.org/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hyperion.list
sudo apt-get update && sudo apt install -y hyperion

# Allow access to serial ports for current user
sudo usermod -a -G dialout ${USER}

#
# 1. Enable "Hyperion" in Gnome Tweak Tool at startup
# 2. Visit http://http://localhost:8090 and import config in Configuration => General
#
```

#### Arduino

1. Fetch the [Adalight Arduino program](https://github.com/hyperion-project/hyperion.ng/blob/master/assets/firmware/arduino/adalight/adalight.ino)
2. Configure according your needs
3. Flash to Arduino Nano
