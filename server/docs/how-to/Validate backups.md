# How-to: Validate backups

Services which are backed up:

- Eve
  - `bjoetiek-backend` (GoCommerce): Images
  - `bjoetiek-db` (Postgres): DB data
  - `goatcounter` (GoatCounter): SQLite DB
  - `keycloak-db` (Postgres): DB data
  - `nc-db` (MariaDB): DB data for Nextcloud
  - `nextcloud` (Nextcloud): User files, config, calendars and addressbooks
- Gandalf
  - N/A
- Kubo
  - `github-backup` (GitHub Backup): All GitHub repo's
  - `glitchtip-db` (Postgres): DB data
  - `ha` (Home Assistant): Config files
  - `librenms-db` (MariaDB): DB data
  - `miniflux-db` (Postgres): DB data
  - `nc-db` (MariaDB): DB data for Nextcloud
  - `nextcloud` (Nextcloud): User files and config
  - `plex` (Plex): Photo's and music

## Validations

To validate the backups, first follow [instructions to mount the archive](Restore%20Borg%20backup.md).

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
# Copy GoatCounter DB to restore point
sudo docker exec borgmatic cp /mnt/borg/mnt/source/goatcounter/db/goatcounter.sqlite3 /mnt/restore

# Validate if backup contains recent site hits.
# The accuracy of this check depens on the activity on your websites.
sudo docker run --rm -v /opt/appdata/borgmatic/borgmatic/restore:/backup alpine sh -c 'apk add sqlite; sqlite3 --table /backup/goatcounter.sqlite3 "select s.link_domain, max(h.hour) from hit_counts h join sites s on h.site_id = s.site_id group by s.link_domain;"'
```

### GoCommerce

```bash
# List 3 newest files in live service.
# List directly on host as the GoCommerce container has no shell.
sudo ls -Alt /opt/appdata/bjoetiek/backend/images | head -n 4

# Compare against 3 newest files in backup
sudo docker exec borgmatic ls -Alt /mnt/borg/mnt/source/bjoetiek/backend/images | head -n 4
```

### Home Assistant

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

### Plex

### Postges

```bash
# Copy all Postgres dumps to the restore point
sudo docker exec borgmatic find /mnt/borg -name "*.pg_dump" -exec cp {} /mnt/restore \;

# Check if backup files is correctly created
sudo docker run --rm -v /opt/appdata/borgmatic/borgmatic/restore:/backup postgres:alpine bash -c 'for f in /backup/*.pg_dump; do echo $f; pg_restore --list $f | head -n 12; echo; done;'
```
