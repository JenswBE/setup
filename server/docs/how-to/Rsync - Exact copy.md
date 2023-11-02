# How-to: Create an exact copy with rsync

```bash
# 1. On target machine
sudo visudo # Add "%sudo   ALL= NOPASSWD:/usr/bin/rsync" or equivalent

# 2. On source machine
# --archive: All files with permissions, etc..
# --human-readable: Output numbers in a human-readable format
# --no-inc-recursive: Ensures correct progress is reported
# --rsync-path: Ensures correct permissions of files
rsync --acls --archive --hard-links --human-readable --info=progress2 --no-inc-recursive --one-file-system --rsync-path="sudo rsync" --verbose --xattrs SOURCE TARGET

# 3. On target machine
sudo visudo # Remove line of step 1
```

Based on:

- https://unix.stackexchange.com/a/490659
- https://unix.stackexchange.com/questions/92123/rsync-all-files-of-remote-machine-over-ssh-without-root-user
