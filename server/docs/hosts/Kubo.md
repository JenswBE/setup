# Kubo

Home NAS

## Scheduled jobs

### Continuous

- Every 5 mins: Nextcloud cron.php (`templates/hosts/kubo/etc/systemd/system/nextcloud-cron.timer`)
- Every 10 mins: Nextcloud generate previews (`templates/hosts/kubo/etc/systemd/system/nextcloud-preview-generator.timer`)

### 01:00 Daily application jobs

- Rescan photos for Nextcloud Maps (`templates/hosts/kubo/etc/systemd/system/nextcloud-maps-scan-photos.timer`)
- Reset MiniFlux feed errors (`templates/hosts/kubo/etc/systemd/system/miniflux-reset-feed-errors.timer`)

### 02:00 Prepare backup

- Dump Glitchtip DB (`templates/hosts/kubo/etc/systemd/system/glitchtip-dump-db.timer`)
- Dump Graylog DB (`templates/hosts/kubo/etc/systemd/system/graylog-dump-mongodb.timer`)
- Dump Miniflux DB (`templates/hosts/kubo/etc/systemd/system/miniflux-dump-db.timer`)
- Dump Nextcloud DB (`templates/hosts/kubo/etc/systemd/system/nextcloud-dump-db.timer`)
- Dump Zabbix DB (`templates/hosts/kubo/etc/systemd/system/zabbix-dump-db.timer`)
- GitHub Backup (`templates/hosts/kubo/etc/systemd/system/github-backup.timer`)

### 03:00 Perform backup

- Run Borgmatic (`templates/hosts/kubo/home/_user_/kubo/borgmatic/borgmatic.d/crontab.txt`)

### 04:00 Perform application updates

- 04:00 Update all Docker containers (`templates/hosts/kubo/etc/systemd/system/docker-update-containers.timer`)
- 04:30 Update all Nextcloud apps (`templates/hosts/kubo/etc/systemd/system/nextcloud-update-apps.timer`)

### System tasks

- 05:00 Update and restart (unattended updates)
- 06:00 First of month: Scrub BTRFS filesystem (`templates/hosts/kubo/etc/systemd/system/btrfs-scrub-*.timer`)
