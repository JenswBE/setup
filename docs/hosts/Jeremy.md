# Jeremy

## Scheduled jobs

### Continuous

- Every 5 mins: Update IP in DNS (`templates/jeremy/home/_user_/jeremy/docker-compose.yml: cloudflare-ddns`)

### 01:00 Daily application jobs

- None

### 02:00 Prepare backup

- None

### 03:00 Perform backup

- None

### 04:00 Perform application updates

- Run Watchtower (`templates/olaf/home/_user_/olaf/docker-compose.yml: watchtower`)

### System tasks

- 05:00 Update and restart (unattended updates)
