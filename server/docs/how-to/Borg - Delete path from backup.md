# How-to: Borg - Delete path from backups

```bash
# Remove path from backups
docker exec borgmatic sh -c "BORG_RSH=\"ssh -p${BORGMATIC_PORT:?} -i /root/.ssh/BorgHost\" \
                             borg recreate ${BORGMATIC_USER:?}@${BORGMATIC_HOST:?}:${BORGMATIC_PATH:?} \
                             -e mnt/source/${PATH_TO_DELETE:?}"

# Reclaim storage
docker exec borgmatic borgmatic compact --progress
```
