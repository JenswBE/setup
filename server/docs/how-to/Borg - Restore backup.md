# How-to: Borg - Restore backup

## From server with borgmatic configured

```bash
# List archives
sudo docker exec borgmatic borgmatic list

# Create mount point
sudo docker exec borgmatic mkdir -p /mnt/borg

# Mount archive
REPO=photos
ARCHIVE=latest
sudo docker exec borgmatic borgmatic mount --repository ${REPO:?} --archive ${ARCHIVE:?} --mount-point /mnt/borg

# Copy required files to host
# "docker cp" works as well, but you won't be able to glob without first tarring the files.
sudo docker exec borgmatic cp /mnt/borg/... /mnt/restore

# Unmount archive
sudo docker exec borgmatic borgmatic umount --mount-point /mnt/borg
```

## From another machine

**Prerequisites:**

- Access to borg repository (e.g. via SSH)
- Passphrase for borg repository

**Process:**

```bash
# Config
set -uo pipefail
BORGBASE_REPO_ID=xxxxxxxx # COMPLETE ME
export BORG_PASSPHRASE='' # COMPLETE ME
BORG_SSH_KEY_NAME='borg_restore'

# Computed
RESTORE_DIR="$(pwd)/restore"
BORG_SSH_KEY_PATH=$(realpath ./${BORG_SSH_KEY_NAME:?})
export BORG_REPO="ssh://${BORGBASE_REPO_ID:?}@${BORGBASE_REPO_ID:?}.repo.borgbase.com/./repo"
export BORG_RSH="ssh -i ${BORG_SSH_KEY_PATH:?}"

# Run borgmatic container
mkdir -p "${RESTORE_DIR:?}"
podman run -it --volume "${RESTORE_DIR:?}:/restore:z" --entrypoint /bin/bash ghcr.io/borgmatic-collective/borgmatic:2.0

# Inside container:
# Generate a new SSH key if needed
ssh-keygen -t ed25519 -N '' -f ${BORG_SSH_KEY_NAME:?}

# Trust the SSH key on the Borg server
cat ${BORG_SSH_KEY_NAME:?}.pub

# List archives
borg list

# List contents of latest archive
BORG_LATEST_ARCHIVE=$(borg list --last 1 --format '{archive}')
borg list ::${BORG_LATEST_ARCHIVE:?}

# Download files from latest archive
cd /restore
borg extract --list ::${BORG_LATEST_ARCHIVE:?} # Extract all
borg extract --list ::${BORG_LATEST_ARCHIVE:?} mnt # Extracts specific file/folder
```
