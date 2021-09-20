# Gandalf

Storage VPS

## Scheduled jobs

### Continuous

- None

### 01:00 Daily application jobs

- None

### 02:00 Prepare backup

- None

### 03:00 Perform backup

- None

### 04:30 Perform application updates

This is later than other hosts to provide a bit more time to backup to Gandalf.

- 04:30 Update all Docker containers (`templates/gandalf/etc/systemd/system/docker-update-containers.timer`)

### System tasks

- 05:00 Update and restart (unattended updates)
