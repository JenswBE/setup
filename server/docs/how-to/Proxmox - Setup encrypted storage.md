1. Install Proxmox with advanced disk config
   - Swap size = RAM size
   - Max root = 20GB
   - Max data = 10GB
1. Remove Enterprise repo and enable `no-subscription` repo's
1. Remove "pve-data" from Datacenter storage
1. Remove "pve-data" from node storage

```bash
# Create a new logical volume
lvcreate -l 90%FREE -n encrypted_data pve

# Install requirements
apt install cryptsetup clevis clevis-luks clevis-systemd

# Create LUKS volume
cryptsetup --verify-passphrase --verbose luksFormat /dev/pve/encrypted_data

# Add to crypttab
echo -e 'data /dev/pve/encrypted_data none netdev' | tr ' ' '\t' >> /etc/crypttab

# Setup Clevis
clevis luks bind -d /dev/pve/encrypted_data tang '{"url": "http://kubo.jensw.eu:7500"}'

# Setup /data mount
cryptsetup luksOpen /dev/pve/encrypted_data data
mkfs.ext4 -L data /dev/mapper/data
mkdir /data
echo -e '/dev/mapper/data /data ext4 defaults 0 1' | tr ' ' '\t' >> /etc/fstab
systemctl daemon-reload
mount -a
```

Add `/data` as new `dir` volume
