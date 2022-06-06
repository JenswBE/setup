# Dual-boot with Full Disk Encryption

## Fedora 36

1. Install Windows and ensure there is empty space for Fedora
2. During installer in "INSTALLATION DESTINATION", enable "Encrypt my data"

# Ubuntu 20.04

Based on

- https://wiki.archlinux.org/title/Dm-crypt/Encryptinganentiresystem#LVMon_LUKS
- https://askubuntu.com/a/293029

```bash
# Settings
BOOT_DEV=/dev/nvme0n1p4
CRYPT_DEV=/dev/nvme0n1p5

# Setup LUKS
sudo cryptsetup luksFormat ${CRYPT_DEV}
sudo cryptsetup open ${CRYPT_DEV} cryptlvm

# Setup LVM
sudo pvcreate /dev/mapper/cryptlvm
sudo vgcreate Linux /dev/mapper/cryptlvm
sudo lvcreate -L 20G Linux -n swap
sudo lvcreate -l 100%FREE Linux -n root

# Create file systems
sudo mkswap /dev/Linux/swap
sudo mkfs.ext4 /dev/Linux/root

# Run Ubuntu installer (Don't reboot!)

# Get UUID of LUKS partition
sudo blkid -o value ${CRYPT_DEV} | head -n 1

# Chroot into new install
sudo mount /dev/Linux/root /mnt
sudo mount ${BOOT_DEV} /mnt/boot
sudo mount --bind /dev /mnt/dev
sudo chroot /mnt

# Mount remaining stuff
mount -t proc proc /proc
mount -t sysfs sys /sys
mount -t devpts devpts /dev/pts

# Setup crypttab
# RELOAD SETTING VARS!
CRYPT_UUID="" # Complete me
cat <<EOF > /etc/crypttab
# <target name> <source device> <key file> <options>
cryptlvm UUID=${CRYPT_UUID} none luks,discard
EOF
cat /etc/crypttab # Validate content
update-initramfs -k all -c
```
