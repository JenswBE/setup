# Configure services

## After `docker compose up -d`

### Borgmatic

1. Execute `ssh-keygen` and create a new ssh key with blank passphrase
2. Add public key to allowed ssh keys at remote host (depending on service)
3. Init repo if required with `sudo docker exec borgmatic borgmatic init`
4. Perform a backup to test the setup with `sudo docker exec borgmatic borgmatic create`
5. Optional: Backup your repo key file with below command:

```bash
sudo docker exec borgmatic borgmatic borg key export /repokey
sudo docker cp borgmatic:/repokey .
```

### GoatCounter

```bash
GC_HOST=stats.jensw.be
GC_USER=$REPLACE_ME
docker compose run --rm goatcounter db create site -createdb -vhost=${GC_HOST} -user.email=${GC_USER}
```

### Home Assistant

To setup a reverse proxy:

1. Setup reverse proxy and point to HA
2. Install add-on `File editor`
3. Edit file `configuration.yml`
```yaml
http:
  # server_host: 127.0.0.1
  use_x_forwarded_for: true
  trusted_proxies: IP_OF_THE_REVERSE_PROXY
```
4. Restart HA

### Keycloak

```bash
# Create initial admin user
docker exec keycloak /opt/jboss/keycloak/bin/add-user-keycloak.sh -u <USERNAME> -p <PASSWORD>
docker restart keycloak
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

# Disable system address book
docker exec -u www-data nextcloud php occ config:app:set dav system_addressbook_exposed --value=no

# Disable unwanted apps
export NEXTCLOUD_APPS_DISABLE=comments,firstrunwizard,photos,weather_status
for NC_APP in ${NEXTCLOUD_APPS_DISABLE};
do
  docker exec -it -u www-data nextcloud php occ app:disable ${NC_APP}
done

# Install usefull apps
export NEXTCLOUD_APPS_INSTALL=apporder,calendar,contacts,groupfolders,notes,previewgenerator,quota_warning,tasks
for NC_APP in ${NEXTCLOUD_APPS_INSTALL};
do
  docker exec -it -u www-data nextcloud php occ app:install ${NC_APP}
done
```

### Paperless

Run `sudo docker compose run --rm paperless createsuperuser`

### Syncthing

- Settings => General => Set `Device Name`
- Settings => General => Set `Default Folder Path` to `/data/`
- Settings => GUI => Set `GUI Authentication User`
- Settings => GUI => Set `GUI Authentication Password`
- Settings => GUI => Set `GUI Theme` to `Dark`
