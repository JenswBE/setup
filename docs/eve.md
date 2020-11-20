# Eve
Hetzner VPS

## Scheduled jobs

### Continuous
- Every 5 mins: Nextcloud cron.php (/systemd/system/nextcloud-cron.timer)
- Every 10 mins: Nextcloud generate previews (/systemd/system/nextcloud-preview-generator.timer)

### 01:00 Daily application jobs
- Dead link checker (DeLiC): Check sites for dead links

### 02:00 Prepare backup
- Dump Nextcloud DB (/systemd/system/nextcloud-dump-db.timer)
- Dump Nextcloud calendars and contacts (/systemd/system/nextcloud-calcardbackup.timer)
- Dump Passit DB (/systemd/system/passit-dump-db.timer)

### 03:00 Perform backup
- Run Borgmatic (conf/borgmatic/borgmatic.d/crontab.txt)

### 04:00 Perform application updates
- 04:00 Run Watchtower (docker-compose.yml)
- 04:30 Update all Nextcloud apps (/systemd/system/nextcloud-update-apps.timer)

### System tasks
- 05:00 Update and restart (locksmith)
