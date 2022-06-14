# How-to: Restore Borg backup

```bash
# List archives
docker exec borgmatic borgmatic list

# Create mount point
docker exec borgmatic mkdir -p /mnt/borg

# Mount archive
ARCHIVE=latest
docker exec borgmatic borgmatic mount --archive ${ARCHIVE:?} --mount-point /mnt/borg

# Copy required files to host
docker exec borgmatic cp /mnt/borg/... /mnt/restore

# Unmount archive
docker exec borgmatic borgmatic umount --mount-point /mnt/borg
```
