# Drivers

## rtl8811au

```bash
# Install rtl8811au drivers
# Based on:
#   - https://docs.alfa.com.tw/Support/Linux/RTL8811AU/
#   - https://github.com/aircrack-ng/rtl8812au
git clone -b v5.6.4.2 https://github.com/aircrack-ng/rtl8812au.git
cd rtl*
sudo dnf update # Important as "dkms" might install a newer kernel, but not modules for e.g. existing wireless devices.
sudo dnf install dkms
sudo make dkms_install
```
