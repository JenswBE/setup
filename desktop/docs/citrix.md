# Citrix

```bash
# Setup distrobox
# See https://github.com/89luca89/distrobox/blob/main/docs/compatibility.md#containers-distros
distrobox-create -Y -i quay.io/toolbx-images/debian-toolbox:12 --name debian-citrix
distrobox-enter debian-citrix

# Download latest Citrix Workspace app
# See https://www.citrix.com/downloads/workspace-app/linux/workspace-app-for-linux-latest.html
wget -O citrix.deb DOWNLOAD_URL
sudo apt install ./citrix.deb
distrobox-export --app ICA

# Right click on .ica file and select "Open With ...".
# Use "Citrix Workspace Engine" and set as default.
```
