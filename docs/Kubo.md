# Olaf

Home NAS

## Scheduled jobs

### Continuous

- None

### 01:00 Daily application jobs

- None

### 02:00 Prepare backup

- None

### 03:00 Perform backup

- Run Borgmatic (`templates/kubo/home/_user_/kubo/borgmatic/borgmatic.d/crontab.txt`)

### 04:00 Perform application updates

- Run Watchtower (`templates/kubo/home/_user_/kubo/docker-compose.yml: watchtower`)

### System tasks

- 05:00 Update and restart (unattended updates)
