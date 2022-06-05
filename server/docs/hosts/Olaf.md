# Olaf

Home NAS

## Scheduled jobs

### Continuous

- Automatically: Update IP in DNS (`templates/olaf/home/_user_/olaf/docker-compose.yml: ddclient`)

### 01:00 Daily application jobs

- None

### 02:00 Prepare backup

- None

### 03:00 Perform backup

- Run Borgmatic (`templates/olaf/home/_user_/olaf/borgmatic/borgmatic.d/crontab.txt`)

### 04:00 Perform application updates

- 04:00 Update all Docker containers (`templates/olaf/etc/systemd/system/docker-update-containers.timer`)

### System tasks

- 05:00 Update and restart (unattended updates)
- 06:00 First of month: Scrub BTRFS filesystem (`templates/olaf/etc/systemd/system/btrfs-scrub.timer`)
