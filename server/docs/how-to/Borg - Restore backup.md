# How-to: Borg - Restore backup

```bash
# List archives
sudo docker exec borgmatic borgmatic list

# Create mount point
sudo docker exec borgmatic mkdir -p /mnt/borg

# Mount archive
ARCHIVE=latest
sudo docker exec borgmatic borgmatic mount --archive ${ARCHIVE:?} --mount-point /mnt/borg

# Copy required files to host
# "docker cp" works as well, but you won't be able to glob without first tarring the files.
sudo docker exec borgmatic cp /mnt/borg/... /mnt/restore

# Unmount archive
sudo docker exec borgmatic borgmatic umount --mount-point /mnt/borg
```
