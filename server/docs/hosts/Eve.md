# Eve

VPS

## Scheduled jobs

### Continuous

- Every 5 mins: Nextcloud cron.php (`templates/hosts/eve/etc/systemd/system/nextcloud-cron.timer`)
- Every 10 mins: Nextcloud generate previews (`templates/hosts/eve/etc/systemd/system/nextcloud-preview-generator.timer`)
- Every 15 mins: IMAP Save Attachments (`templates/hosts/eve/etc/systemd/system/isa-rclone.timer`)

### 01:00 Daily application jobs

- Dead link checker (DeLiC): Check sites for dead links (`templates/hosts/eve/home/_user_/eve/delic/config.yml`)
- Rescan photos for Nextcloud Maps (`templates/hosts/eve/etc/systemd/system/nextcloud-maps-scan-photos.timer`)

### 02:00 Prepare backup

- Dump Bjoetiek DB (`templates/hosts/eve/etc/systemd/system/bjoetiek-dump-db.timer`)
- Dump Goatcounter DB (`templates/hosts/eve/etc/systemd/system/goatcounter-dump-db.timer`)
- Dump Keycloak DB (`templates/hosts/eve/etc/systemd/system/keycloak-dump-db.timer`)
- Dump Nextcloud DB (`templates/hosts/eve/etc/systemd/system/nextcloud-dump-db.timer`)
- Dump Nextcloud calendars and contacts (`templates/hosts/eve/etc/systemd/system/nextcloud-calcardbackup.timer`)
- Dump Paperless-ngx DB (`templates/hosts/eve/etc/systemd/system/paperless-dump-db.timer`)
- Dump Uptime Kuma DB (`templates/hosts/eve/etc/systemd/system/uptime-kuma-dump-db.timer`)
- Dump Vaultwarden DB (`templates/hosts/eve/etc/systemd/system/vaultwarden-dump-db.timer`)
- Dump Wiki.js DB (`templates/hosts/eve/etc/systemd/system/wikijs-dump-db.timer`)
- Dump WTech Directus DB (`templates/hosts/eve/etc/systemd/system/wtech-directus-dump-db.timer`)

### 03:00 Perform backup

- Run Borgmatic (`templates/hosts/eve/home/_user_/eve/borgmatic/borgmatic.d/crontab.txt`)

### 04:00 Perform application updates

- 04:00 Update all Docker containers (`templates/hosts/eve/etc/systemd/system/docker-update-containers.timer`)
- 04:30 Update all Nextcloud apps (`templates/hosts/eve/etc/systemd/system/nextcloud-update-apps.timer`)

### System tasks

- 05:00 Update and restart (unattended updates)
