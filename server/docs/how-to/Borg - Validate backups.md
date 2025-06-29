# How-to: Validate backups

Services which are backed up:

- Eve
  - `bjoetiek-directus` (Directus): Uploaded content
  - `bjoetiek-directus-db` (Postgres): DB data
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
- Kubo
  - `github-backup` (GitHub Backup): All GitHub repo's
  - `graylog-mongodb` (MongoDB): DB data
  - `ha` (Home Assistant): Config files
  - `immich-db` (Postgres): DB data for Immich
  - `unifi-mongodb` (MongoDB): DB data
  - `zabbix-db` (Postgres): DB data

## Validations

To validate the backups, first follow [instructions to mount the archive](Borg%20-%20Restore%20backup.md).
Next, make following preparations:

```bash
# Make sure the restore directory of Borgmatic is empty
sudo docker exec borgmatic sh -c 'rm -rf /mnt/restore/*'

# Set env vars
APPDATA_DIR=/opt/appdata
```

### Directus

#### Bjoetiek Y

```bash
# List 3 newest files in live service.
sudo docker exec bjoetiek-directus ls -Alt /directus/uploads | head -n 4

# Compare against 3 newest files in backup
sudo docker exec borgmatic ls -Alt /mnt/borg/mnt/source/bjoetiek/directus/uploads | head -n 4
```

#### Kristof Coenen

```bash
# List 3 newest files in live service.
sudo docker exec kristofcoenen-directus ls -Alt /directus/uploads | head -n 4

# Compare against 3 newest files in backup
sudo docker exec borgmatic ls -Alt /mnt/borg/mnt/source/kristofcoenen/directus/uploads | head -n 4
```

#### Tuinfeest

```bash
# List 3 newest files in live service.
sudo docker exec tuinfeest-directus ls -Alt /directus/uploads | head -n 4

# Compare against 3 newest files in backup
sudo docker exec borgmatic ls -Alt /mnt/borg/mnt/source/tuinfeest/directus/uploads | head -n 4
```

#### WTech

```bash
# List 3 newest files in live service.
sudo docker exec wtech-directus ls -Alt /directus/uploads | head -n 4

# Compare against 3 newest files in backup
sudo docker exec borgmatic ls -Alt /mnt/borg/mnt/source/wtech/directus/uploads | head -n 4
```

### GitHub Backup

```bash
# List backup source
sudo docker compose run -it --entrypoint "/bin/sh -c" github-backup "/usr/bin/find /backup -type d -name refs -exec sh -c 'cd {}/..; git log -1 --all --date-order --format=\"%cI => \${PWD##*/}\"' \; | sort -r | head -n 3"

# List backup contents
# Since Borgmatic uses BusyBox which doesn't support "execdir",
# we have to use the "cd {}/.." trick instead.
sudo docker exec borgmatic apk add git
sudo docker exec borgmatic sh -c "find /mnt/borg/mnt/source/github-backup/backup -type d -name refs -exec bash -c 'cd {}/..; git log -1 --all --date-order --format=\"%cI => \${PWD##*/}\"' \; | sort -r | head -n 3"
```

### GoatCounter

```bash
# Copy DB to restore point
sudo docker exec borgmatic cp /mnt/borg/mnt/source/goatcounter/db/goatcounter.backup.sqlite3 /mnt/restore/goatcounter.sqlite3

# Validate if backup contains recent site hits.
# The accuracy of this check depens on the activity on your websites.
sudo docker run --pull always --rm -v ${APPDATA_DIR:?}/borgmatic/borgmatic/restore:/backup alpine sh -c 'apk add sqlite; sqlite3 --table /backup/goatcounter.sqlite3 "SELECT s.link_domain, max(h.hour) FROM hit_counts h JOIN sites s ON h.site_id = s.site_id GROUP BY s.link_domain;"'
```

### Graylog

```bash
# Copy DB to restore point
sudo docker exec borgmatic cp /mnt/borg/mnt/source/graylog/mongodb/graylog/traffic.bson /mnt/restore/graylog_traffic.bson

# Validate if backup contains recent data.
sudo docker run --rm -v ${APPDATA_DIR:?}/borgmatic/borgmatic/restore:/backup docker.io/library/mongo sh -c "bsondump /backup/graylog_traffic.bson | jq --slurp '.' | jq '.[].bucket.\"\$date\".\"\$numberLong\"' | sort -r | head -n1 | cut -c2-11 | sed '1s/^/@/' | date -f-"
```

### Home Assistant

```bash
# Listed entries should be recent
sudo docker exec borgmatic ls -ltc /mnt/borg/mnt/source/home-automation/home-assistant/config/
```

### Immich

COMPLETE_ME

### MariaDB

```bash
# Check backup date of all MariaDB dumps
sudo docker exec borgmatic find /mnt/borg -name "*.sqldump" -exec echo {} \; -exec tail -n1 {} \; -exec echo Number of tables: \; -exec bash -c "grep -F 'CREATE TABLE' {} | wc -l" \;
```

### Nextcloud

#### Config file

```bash
# List size and change date of live config file
sudo docker exec nextcloud ls -Alt config/config.php

# Compare against config file in backup
sudo docker exec borgmatic ls -Alt /mnt/borg/mnt/source/nextcloud/config/config/config.php
```

#### User files

```bash
# List size and change date of 3 newest files before today
# Since Borgmatic uses BusyBox which doesn't support "newermt", we calculate the minutes since midnight locally.
# This ensures a correct comparison. Based on https://stackoverflow.com/a/30374251
MINS_SINCE_MIDNIGHT=$(( $(date "+10#%H * 60 + 10#%M") ))
sudo docker exec nextcloud sh -c "find data -type f -mmin +${MINS_SINCE_MIDNIGHT:?} -exec stat -c '%Y %n' {} \; | sort -nr | head -n 3 | cut -d' ' -f2- | tr \\\n \\\0 | xargs -0 ls -lah"

# Compare against files in backup
sudo docker exec borgmatic sh -c "find /mnt/borg/mnt/source/nextcloud/data -type f -mmin +${MINS_SINCE_MIDNIGHT:?} -exec stat -c '%Y %n' {} \; | sort -nr | head -n 3 | cut -d' ' -f2- | tr \\\n \\\0 | xargs -0 ls -lah"
```

#### Calendars and contacts

```bash
# Check if exports were created for past backup
sudo docker exec borgmatic ls -Alth /mnt/borg/mnt/source/nextcloud/calcardbackup/calcardbackup_overwrite | head -n 50
```

### Paperless

```bash
# List size and change date of 3 newest files before today
# Since Borgmatic uses BusyBox which doesn't support "newermt", we calculate the minutes since midnight locally.
# This ensures a correct comparison. Based on https://stackoverflow.com/a/30374251
MINS_SINCE_MIDNIGHT=$(( $(date "+10#%H * 60 + 10#%M") ))
sudo docker exec paperless sh -c "find /usr/src/paperless/media -type f -mmin +${MINS_SINCE_MIDNIGHT:?} -exec stat -c '%Y %n' {} \; | sort -nr | head -n 3 | cut -d' ' -f2- | tr \\\n \\\0 | xargs -0 ls -lah"

# Compare against files in backup
sudo docker exec borgmatic sh -c "find /mnt/borg/mnt/source/paperless/docs -type f -mmin +${MINS_SINCE_MIDNIGHT:?} -exec stat -c '%Y %n' {} \; | sort -nr | head -n 3 | cut -d' ' -f2- | tr \\\n \\\0 | xargs -0 ls -lah"
```

### Plex

```bash
# List size and change date of 3 newest files before today
# Since Plex doesn't support "find -newermt", we calculate the minutes since midnight locally.
# This ensures a correct comparison. Based on https://stackoverflow.com/a/30374251
MINS_SINCE_MIDNIGHT=$(( $(date "+10#%H * 60 + 10#%M") ))
sudo docker exec plex sh -c "find /data/Photos -type f -mmin +${MINS_SINCE_MIDNIGHT:?} -exec stat -c '%Y %n' {} \; | sort -nr | head -n 3 | cut -d' ' -f2- | tr \\\n \\\0 | xargs -0 ls -lah"

# Compare against files in backup
sudo docker exec borgmatic sh -c "find /mnt/borg/mnt/source/plex/photos -type f -mmin +${MINS_SINCE_MIDNIGHT:?} -exec stat -c '%Y %n' {} \; | sort -nr | head -n 3 | cut -d' ' -f2- | tr \\\n \\\0 | xargs -0 ls -lah"

# Repeat the same for music
sudo docker exec plex sh -c "find /data/media/Music -type f -mmin +${MINS_SINCE_MIDNIGHT:?} -exec stat -c '%Y %n' {} \; | sort -nr | head -n 3 | cut -d' ' -f2- | tr \\\n \\\0 | xargs -0 ls -lah"
sudo docker exec borgmatic sh -c "find /mnt/borg/mnt/source/plex/music -type f -mmin +${MINS_SINCE_MIDNIGHT:?} -exec stat -c '%Y %n' {} \; | sort -nr | head -n 3 | cut -d' ' -f2- | tr \\\n \\\0 | xargs -0 ls -lah"
```

### Postgres

```bash
# Copy all Postgres dumps to the restore point
sudo docker exec borgmatic find /mnt/borg -name "*.pg_dump" -exec cp {} /mnt/restore \;

# Check if backup files is correctly created
sudo docker run --pull always --rm -v ${APPDATA_DIR:?}/borgmatic/borgmatic/restore:/backup postgres:alpine bash -c 'for f in /backup/*.pg_dump; do echo $f; pg_restore --list $f | head -n 12; echo; done;'
```

### Unifi controller

```bash
# Copy DB to restore point
sudo docker exec borgmatic cp /mnt/borg/mnt/source/unifi/mongodb/unifi/unifi/event.bson /mnt/restore/unifi_event.bson
sudo docker exec borgmatic cp /mnt/borg/mnt/source/unifi/mongodb/unifi_stat/unifi_stat/stat_5minutes.bson /mnt/restore/unifi_stat_5min.bson

# Validate if backup contains recent data.
sudo docker run --rm -v ${APPDATA_DIR:?}/borgmatic/borgmatic/restore:/backup docker.io/library/mongo sh -c "bsondump /backup/unifi_event.bson | jq --slurp '.' | jq '.[].datetime.\"\$date\".\"\$numberLong\"' | sort -r | head -n1 | cut -c2-11 | sed '1s/^/@/' | date -f-"
sudo docker run --rm -v ${APPDATA_DIR:?}/borgmatic/borgmatic/restore:/backup docker.io/library/mongo sh -c "bsondump /backup/unifi_stat_5min.bson | jq --slurp '.' | jq '.[].datetime.\"\$date\".\"\$numberLong\"' | sort -r | head -n1 | cut -c2-11 | sed '1s/^/@/' | date -f-"
```

### Vaultwarden

Based on https://github.com/dani-garcia/vaultwarden/wiki/Backing-up-your-vault

```bash
# Copy DB to restore point
sudo docker exec borgmatic cp /mnt/borg/mnt/source/vaultwarden/data/db.backup.sqlite3 /mnt/restore/vaultwarden.sqlite3

# Validate if backup contains recent devices.
# The accuracy of this check depens on how recently a device used Vaultwarden.
sudo docker run --pull always --rm -v ${APPDATA_DIR:?}/borgmatic/borgmatic/restore:/backup alpine sh -c 'apk add sqlite; sqlite3 --table /backup/vaultwarden.sqlite3 "SELECT updated_at, name FROM devices ORDER BY updated_at DESC LIMIT 3;"'

# Listed entries should be recent
sudo docker exec borgmatic ls -ltc /mnt/borg/mnt/source/vaultwarden/data/
```

### Wiki.js

```bash
# Check if recent files are in export
sudo docker exec borgmatic bash -c 'ls -Alth /mnt/borg/mnt/source/wikijs/backup/*'
```
