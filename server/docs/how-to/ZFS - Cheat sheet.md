# ZFS

## Mount encrypted dataset

```bash
# List available pools
sudo zpool import -f

# Import pool
POOL_NAME=main
sudo zpool import -f ${POOL_NAME:?}

# Load encryption key
sudo zfs load-key ${POOL_NAME:?}

# Mount pool
sudo zfs mount -R ${POOL_NAME:?}

# List datasets
sudo zfs list
```

## Unmount encrypted dataset

```bash
# Mount and unload encryption key
sudo zfs unmount -u ${POOL_NAME:?}

# If needed, manually unload encryption key
sudo zfs unload-key ${POOL_NAME:?}

# Export pool
sudo zpool export ${POOL_NAME:?}
```
