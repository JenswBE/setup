# How-to: Borg - Setup remote

Create `.ssh/authorized_keys` with following contents:

```
command="borg serve --append-only --restrict-to-repository borg/CLIENT_HOSTNAME",restrict PUBLIC_KEY
```

Based on:

- https://borgbackup.readthedocs.io/en/stable/deployment/hosting-repositories.html
