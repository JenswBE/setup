# Olaf

Home NAS

## Scheduled jobs

### Continuous

- Every 5 mins: Nextcloud cron.php (`templates/eve/etc/systemd/system/nextcloud-cron.timer`)
- Every 10 mins: Nextcloud generate previews (`templates/eve/etc/systemd/system/nextcloud-preview-generator.timer`)

### 01:00 Daily application jobs

- Rescan photos for Nextcloud Maps (`templates/kubo/etc/systemd/system/nextcloud-maps-scan-photos.timer`)

### 02:00 Prepare backup

- Dump Nextcloud DB (`templates/eve/etc/systemd/system/nextcloud-dump-db.timer`)

### 03:00 Perform backup

- Run Borgmatic (`templates/kubo/home/_user_/kubo/borgmatic/borgmatic.d/crontab.txt`)

### 04:00 Perform application updates

- 04:00 Update all Docker containers (`templates/kubo/etc/systemd/system/docker-update-containers.timer`)
- 04:30 Update all Nextcloud apps (`templates/eve/etc/systemd/system/nextcloud-update-apps.timer`)

### System tasks

- 05:00 Update and restart (unattended updates)
