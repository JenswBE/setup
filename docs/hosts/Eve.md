# Eve

Hetzner VPS

## Scheduled jobs

### Continuous

- Every 5 mins: Nextcloud cron.php (`templates/eve/etc/systemd/system/nextcloud-cron.timer`)
- Every 10 mins: Nextcloud generate previews (`templates/eve/etc/systemd/system/nextcloud-preview-generator.timer`)
- Every 15 mins: IMAP Save Attachments (`templates/eve/etc/systemd/system/isa-rclone.timer`)

### 01:00 Daily application jobs

- Dead link checker (DeLiC): Check sites for dead links (`templates/eve/home/_user_/eve/delic/config.yml`)
- Rescan photos for Nextcloud Maps (`templates/eve/etc/systemd/system/nextcloud-maps-scan-photos.timer`)

### 02:00 Prepare backup

- Dump Bjoetiek DB (`templates/eve/etc/systemd/system/bjoetiek-dump-db.timer`)
- Dump Nextcloud DB (`templates/eve/etc/systemd/system/nextcloud-dump-db.timer`)
- Dump Nextcloud calendars and contacts (`templates/eve/etc/systemd/system/nextcloud-calcardbackup.timer`)
- Dump Passit DB (`templates/eve/etc/systemd/system/passit-dump-db.timer`)
- Dump SnipeIT DB (`templates/eve/etc/systemd/system/snipe-it-dump-db.service`)

### 03:00 Perform backup

- Run Borgmatic (`templates/eve/home/_user_/eve/borgmatic/borgmatic.d/crontab.txt`)

### 04:00 Perform application updates

- 04:00 Update all Docker containers (`templates/eve/etc/systemd/system/docker-update-containers.timer`)
- 04:30 Update all Nextcloud apps (`templates/eve/etc/systemd/system/nextcloud-update-apps.timer`)

### System tasks

- 05:00 Update and restart (unattended updates)
