# How-to: Restore Postgres db

```bash
DBNAME=
docker exec ${DBNAME}-db /bin/sh -c "pg_restore --verbose --format=c --dbname=${DBNAME} --username=${DBNAME} /backup/${DBNAME}.pg_dump"
```
