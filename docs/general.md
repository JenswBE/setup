# General

## App data naming convention
`<CATEGORY>/<SERVICE>/<FOLDER>`
E.g. `nextcloud/mariadb/data`

## Borgmatic
```bash
# Export repo key to ~/eve/borgmatic/borgmatic.d/repokey.html
docker exec borgmatic sh -c "BORG_RSH=\"ssh -p${BORGMATIC_PORT:?} -i /root/.ssh/${HOSTNAME:?}\" \
                             borg key export --qr-html ${BORGMATIC_USER:?}@${BORGMATIC_HOST:?}:${BORGMATIC_PATH:?} \
                             /etc/borgmatic.d/repokey.html"
```