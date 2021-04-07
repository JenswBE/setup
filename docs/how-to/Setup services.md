# Configure services

## After `docker-compose up -d`

### Borgmatic

1. Execute `ssh-keygen` and create a new ssh key with blank passphrase
2. Add public key to allowed ssh keys at remote host (depending on service)
3. Init repo if required with `docker exec borgmatic sh -c "borgmatic --init --encryption repokey-blake2"`
4. Perform a backup to test the setup with `docker exec borgmatic sh -c "borgmatic --verbosity 1"`
5. Optional: Backup your repo key file with below command. Your file will be available at `borgmatic/borgmatic.d/repokey.html`.

```bash
# Export repo key to ~/eve/borgmatic/borgmatic.d/repokey.html
docker exec borgmatic sh -c "BORG_RSH=\"ssh -p${BORGMATIC_PORT:?} -i /root/.ssh/BorgHost\" \
                             borg key export --qr-html ${BORGMATIC_USER:?}@${BORGMATIC_HOST:?}:${BORGMATIC_PATH:?} \
                             /etc/borgmatic.d/repokey.html"
```

### Nextcloud

```bash
# Set trusted domains
docker exec -u www-data nextcloud php occ config:system:set trusted_domains 0 --value="${NEXTCLOUD_DOMAIN:?}"
docker exec -u www-data nextcloud php occ config:system:set trusted_domains 1 --value="${NEXTCLOUD_DOMAIN_TF:?}"

# Fix reverse proxy handling
docker exec -u www-data nextcloud php occ config:system:set overwriteprotocol --value="https"
docker exec -u www-data nextcloud php occ config:system:set trusted_proxies 0 --value="172.16.0.0/12"

# Disable skeleton dir (default files)
docker exec -u www-data nextcloud php occ config:system:set skeletondirectory --value=""

# Disable unwanted apps
export NEXTCLOUD_APPS_DISABLE=firstrunwizard
for NC_APP in ${NEXTCLOUD_APPS_DISABLE};
do
  docker exec -it -u www-data nextcloud php occ app:disable ${NC_APP}
done

# Install usefull apps
export NEXTCLOUD_APPS_INSTALL=contacts,calendar,tasks,notes,groupfolders,quota_warning,previewgenerator,apporder
for NC_APP in ${NEXTCLOUD_APPS_INSTALL};
do
  docker exec -it -u www-data nextcloud php occ app:install ${NC_APP}
done
```

### Plex

Go to https://app.plex.tv to setup following libraries:

- Films
  - /data/media/Movies
  - /data/optimized/movies
  - /data/media/Nazien
- TV Series
  - /data/media/TV Shows
  - /data/optimized/shows
  - /data/media/Nazien
- Foto's
  - /data/media/Photos
- Muziek
  - /data/media/Music

### Syncthing

- Settings => General => Set `Device Name`
- Settings => General => Set `Default Folder Path` to `/data/`
- Settings => GUI => Set `GUI Authentication User`
- Settings => GUI => Set `GUI Authentication Password`
- Settings => GUI => Set `GUI Theme` to `Dark`

### Transmission

1. Set correct permission with `sudo chown 233:233 /media/data/services/transmission/`
2. Go through online settings

- Category Torrents
  - Set "Download to" to `/downloads`
  - Set "Directory for incomplete files" to `/running`
  - Set "Stop seeding at ratio" to 3
- Category Queue
  - Set "Download Queue Size" to 10
