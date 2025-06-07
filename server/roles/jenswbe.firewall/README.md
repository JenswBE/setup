# Firewall

## Debug firewall issues

### Check config

```bash
# List all for default zone
sudo firewall-cmd --list-all

# List for active zones
sudo firewall-cmd --get-active-zones
sudo firewall-cmd --list-all --zone local
sudo firewall-cmd --list-all --zone docker
```

### Check logs

```bash
sudo firewall-cmd --set-log-denied all
sudo journalctl -x -e
sudo firewall-cmd --set-log-denied off
```
