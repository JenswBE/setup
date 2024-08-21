# Install Fedora Atomic KDE (Kinoite) for Maria

```bash
# Automatic system updates
sudo tee /etc/rpm-ostreed.conf <<EOF
# Entries in this file show the compile time defaults.
# You can change settings by editing this file.
# For option meanings, see rpm-ostreed.conf(5).

[Daemon]
AutomaticUpdatePolicy=stage
IdleExitTimeout=60
EOF
sudo mkdir -p /etc/systemd/system/rpm-ostreed-automatic.timer.d
sudo tee /etc/systemd/system/rpm-ostreed-automatic.timer.d/10-reduce-on-boot-sec.conf <<EOF
[Timer]
OnBootSec=10m
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now rpm-ostreed-automatic.timer
sudo systemctl enable --now rpm-ostree-countme.timer

# Install Libreoffice
sudo flatpak install org.libreoffice.LibreOffice

# Install VLC
sudo flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
sudo flatpak --assumeyes --noninteractive --or-update install org.videolan.VLC

# Install Google Chrome
sudo tee /etc/yum.repos.d/google-chrome.repo > /dev/null <<EOF
[google-chrome]
name=google-chrome
baseurl=https://dl.google.com/linux/chrome/rpm/stable/x86_64
enabled=1
gpgcheck=0
gpgkey=https://dl.google.com/linux/linux_signing_key.pub
EOF
sudo rpm-ostree refresh-md
sudo rpm-ostree install google-chrome-stable

# Install eID middleware and viewer
# See https://github.com/Fedict/eid-mw/issues/206
wget -O Downloads/eid-repo.rpm https://eid.belgium.be/sites/default/files/software/eid-archive-fedora-2021-1.noarch.rpm
sudo rpm-ostree install ./Downloads/eid-repo.rpm
sudo rpm-ostree override remove opensc
systemctl reboot
sudo rpm-ostree install eid-mw eid-viewer
```
