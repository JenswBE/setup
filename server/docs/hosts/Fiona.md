# Fiona

Low-power home server

## Scheduled jobs

### Continuous

- None

### 01:00 Daily application jobs

- None

### 02:00 Prepare backup

- Dump Unifi DB (`templates/hosts/fiona/etc/systemd/system/unifi-dump-mongodb.timer`)

### 03:00 Perform backup

- Run Borgmatic (`templates/hosts/fiona/home/_user_/fiona/borgmatic/borgmatic.d/crontab.txt`)

### 04:00 Perform application updates

- 04:00 Update all Docker containers (`templates/hosts/fiona/etc/systemd/system/docker-update-containers.timer`)

### System tasks

- 05:00 Update and restart (unattended updates)
