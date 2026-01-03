# How-to: Validate backups

Services which are backed up:

- Eve
  - `bjoetiek-directus` (Directus): Uploaded content
  - `bjoetiek-directus-db` (Postgres): DB data
  - `clementines-db` (CouchDB): DB data ==> TODO
  - `goatcounter` (GoatCounter): SQLite DB
  - `keycloak-db` (Postgres): DB data
  - `kristofcoenen-directus` (Directus): Uploaded content
  - `kristofcoenen-directus-db` (Postgres): DB data
  - `miniflux-db` (Postgres): DB data
  - `nc-db` (MariaDB): DB data for Nextcloud
  - `nextcloud` (Nextcloud): User files, config, calendars and addressbooks
  - `paperless` (Paperless-ngx): Files
  - `paperless-db` (Postgres): DB data
  - `tuinfeest-directus` (Directus): Uploaded content
  - `tuinfeest-directus-db` (Postgres): DB data
  - `vaultwarden` (Vaultwarden): SQLite DB and data
  - `wikijs` (Wiki.js): Data (human readable backup format like Markdown)
  - `wikijs-db` (Postgres): DB data
  - `wtech-directus` (Directus): Uploaded content
  - `wtech-directus-db` (Postgres): DB data
- Kubo Media
  - `immich`: Uploaded and archived photos
  - `immich-db`: Postgres DB data
  - `jellyfin`: Music files
- Kubo Private
  - `github-backup` (GitHub Backup): All GitHub repo's
  - `unifi-mongodb` (MongoDB): DB data
  - `ha` (Home Assistant): Config files => TODO

## Prepare

To prepare for the validations, source or copy/paste script `Borg - Validate backups.sh`

## Eve

```bash
# === bjoetiek-directus: Uploaded content ===
compare_actual_backup_flat bjoetiek-directus /directus/uploads bjoetiek_y directus/uploads

# === bjoetiek-directus-db: Postgres DB data ===
validate_postgres bjoetiek_y directus/dbdump/bjoetiek-directus.pg_dump

# === goatcounter: SQLite DB ===
# Copy DB to restore point
borgmatic_mount goatcounter db
sudo docker exec borgmatic cp /mnt/borg/mnt/source/goatcounter/db/goatcounter.backup.sqlite3 /mnt/restore/goatcounter.sqlite3
borgmatic_umount

# Validate if backup contains recent site hits.
# The accuracy of this check depens on the activity on your websites.
sudo docker run --pull always --rm -v ${APPDATA_DIR:?}/borgmatic/borgmatic/restore:/backup alpine sh -c 'apk add sqlite; sqlite3 --table /backup/goatcounter.sqlite3 "SELECT s.link_domain, max(h.hour) FROM hit_counts h JOIN sites s ON h.site_id = s.site_id GROUP BY s.link_domain;"'

# === keycloak-db: Postgres DB data ===
validate_postgres keycloak dbdump/keycloak.pg_dump

# === kristofcoenen-directus: Uploaded content ===
compare_actual_backup_flat kristofcoenen-directus /directus/uploads kristofcoenen directus/uploads

# === kristofcoenen-directus-db: Postgres DB data ===
validate_postgres kristofcoenen directus/dbdump/kristofcoenen-directus.pg_dump

# === miniflux-db: Postgres DB data ===
validate_postgres miniflux dbdump/miniflux.pg_dump

# === nc-db: Postgres DB data ===
borgmatic_mount nextcloud dbdump
sudo docker exec borgmatic find /mnt/borg/mnt/source/nextcloud/dbdump -name "*.sqldump" -exec echo {} \; -exec tail -n1 {} \; -exec echo Number of tables: \; -exec bash -c "grep -F 'CREATE TABLE' {} | wc -l" \;
borgmatic_umount

# === nextcloud: Config, user files, calendars and addressbooks ===
# Live config file
borgmatic_mount nextcloud config
sudo docker exec nextcloud ls -Alt config/config.php
sudo docker exec borgmatic ls -Alt /mnt/borg/mnt/source/nextcloud/config/config/config.php
borgmatic_umount
# User files
compare_actual_backup_recursive nextcloud /var/www/html/data nextcloud data
# Calendars and addressbooks
borgmatic_mount nextcloud calcardbackup
sudo docker exec borgmatic ls -Alth /mnt/borg/mnt/source/nextcloud/calcardbackup/calcardbackup_overwrite | head -n 20
borgmatic_umount

# === paperless: Files ===
compare_actual_backup_flat paperless /usr/src/paperless/media/documents/originals documents docs/documents/originals
compare_actual_backup_flat paperless /usr/src/paperless/export documents export

# === paperless-db: Postgres DB data ===
validate_postgres documents dbdump/paperless.pg_dump

# === tuinfeest-directus: Uploaded content ===
compare_actual_backup_flat tuinfeest-directus /directus/uploads tuinfeest directus/uploads

# === tuinfeest-directus-db: Postgres DB data ===
validate_postgres tuinfeest directus/dbdump/tuinfeest-directus.pg_dump

# === vaultwarden: SQLite DB and data ===
# Based on https://github.com/dani-garcia/vaultwarden/wiki/Backing-up-your-vault
# DB (The accuracy of this check depens on how recently a device used Vaultwarden.)
borgmatic_mount vaultwarden data
sudo docker exec borgmatic cp /mnt/borg/mnt/source/vaultwarden/data/db.backup.sqlite3 /mnt/restore/vaultwarden.sqlite3
sudo docker run --pull always --rm -v ${APPDATA_DIR:?}/borgmatic/borgmatic/restore:/backup alpine sh -c 'apk add sqlite; sqlite3 --table /backup/vaultwarden.sqlite3 "SELECT updated_at, name FROM devices ORDER BY updated_at DESC LIMIT 3;"'
# Data (Listed entries should be recent)
sudo docker exec borgmatic ls -ltc /mnt/borg/mnt/source/vaultwarden/data/
borgmatic_umount

# === wikijs: Data (human readable backup format like Markdown) ===
compare_actual_backup_recursive wikijs /backup wikijs backup

# === wikijs-db: Postgres DB data ===
validate_postgres wikijs dbdump/wikijs.pg_dump

# === wtech-directus: Uploaded content ===
compare_actual_backup_flat wtech-directus /directus/uploads wtech directus/uploads

# === wtech-directus-db: Postgres DB data ===
validate_postgres wtech directus/dbdump/wtech-directus.pg_dump
```

## Kubo Media

```bash
# === immich: Uploaded and archived photos ===
# Note: Immich's data folder has submounts. Therefore, the source of the first check might have newer files than the backup.
compare_actual_backup_recursive immich /usr/src/app/upload photos immich/data
compare_actual_backup_recursive immich /usr/src/app/upload/library photos truenas/immich/library
compare_actual_backup_recursive immich /usr/src/app/upload/upload photos truenas/immich/upload
compare_actual_backup_recursive immich /external/archive photos truenas/archive

# === immich-db: Postgres DB data ===
validate_postgres photos immich/dbdump/immich.pg_dumpall

# === jellyfin: Music files ===
compare_actual_backup_recursive jellyfin /media/Music music bulk
```

## Kubo Private

```bash
# === github-backup: All GitHub repo's ===
# Mount repo
borgmatic_mount github_backup backup

# List backup source
sudo docker compose run -it --entrypoint "/bin/sh -c" github-backup "/usr/bin/find /backup -mindepth 1 -maxdepth 1 -type d -exec sh -c 'cd {}; git log -1 --all --date-order --format=\"%cI => \${PWD##*/}\"' \; | sort -r | head -n 3"

# List backup contents
sudo docker exec borgmatic apk add git
sudo docker exec borgmatic sh -c "find /mnt/borg/mnt/source/github_backup/backup -mindepth 1 -maxdepth 1 -type d -exec bash -c 'cd {}; git log -1 --all --date-order --format=\"%cI => \${PWD##*/}\"' \; | sort -r | head -n 3"

# Unmount repo
borgmatic_umount

# === unifi-mongodb: MongoDB data ===
# Copy DB to restore point
borgmatic_mount unifi mongodb
sudo docker exec borgmatic cp /mnt/borg/mnt/source/unifi/mongodb/unifi/unifi/event.bson /mnt/restore/unifi_event.bson
sudo docker exec borgmatic cp /mnt/borg/mnt/source/unifi/mongodb/unifi_stat/unifi_stat/stat_5minutes.bson /mnt/restore/unifi_stat_5min.bson
borgmatic_umount

# Validate if backup contains recent data.
sudo docker run --rm -v ${APPDATA_DIR:?}/borgmatic/borgmatic/restore:/backup docker.io/library/mongo sh -c "bsondump /backup/unifi_event.bson | jq --slurp '.' | jq '.[].datetime.\"\$date\".\"\$numberLong\"' | sort -r | head -n1 | cut -c2-11 | sed '1s/^/@/' | date -f-"
sudo docker run --rm -v ${APPDATA_DIR:?}/borgmatic/borgmatic/restore:/backup docker.io/library/mongo sh -c "bsondump /backup/unifi_stat_5min.bson | jq --slurp '.' | jq '.[].datetime.\"\$date\".\"\$numberLong\"' | sort -r | head -n1 | cut -c2-11 | sed '1s/^/@/' | date -f-"
```
