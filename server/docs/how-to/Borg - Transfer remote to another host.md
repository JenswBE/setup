# How-to: Borg - Transfer remote to another host.

## Borg 1.x

```bash
# scp repo contents from source to target
scp -r SOURCE_REPO TARGET_REPO

# Update borgmatic config

# Validate borgmatic (press "y" + enter if hangs)
sudo docker exec -it borgmatic borgmatic rinfo
```
