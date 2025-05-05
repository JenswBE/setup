# Android tools

Based on https://discussion.fedoraproject.org/t/how-to-use-adb-android-debugging-bridge-on-silverblue/2475

```bash
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
```
