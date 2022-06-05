# How-to: Restore Borg backup

```bash
# List archives
docker exec borgmatic sh -c "borgmatic list"

# Create mount point
docker exec borgmatic sh -c "mkdir /mnt/borg"

# Mount archive
ARCHIVE=latest
docker exec borgmatic sh -c "borgmatic mount --archive ${ARCHIVE} --mount-point /mnt/borg"

# Copy required files to host
docker exec borgmatic sh -c "cp /mnt/borg/... /mnt/restore"

# Unmount archive
docker exec borgmatic sh -c "borgmatic umount --mount-point /mnt/borg"
```