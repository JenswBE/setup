# How-to: Borg - Setup remote

## Configure remote SSH access

Create `.ssh/authorized_keys` with following contents:

```
command="borg serve --append-only --restrict-to-repository borg/CLIENT_HOSTNAME",restrict PUBLIC_KEY
```

Based on:
- https://borgbackup.readthedocs.io/en/stable/deployment/hosting-repositories.html

## Init repo

Run the following commands

```bash
# Config
REPO_NAME="" # E.g. knowledge_base

# Ensure Borgmatic has the latest mounts and configs
docker compose --profile scheduled up -d

# Init the remote repo
docker compose exec borgmatic borgmatic init --repo ${REPO_NAME:?}

# Create a first backup
docker compose exec borgmatic borgmatic create --repo ${REPO_NAME:?}
```
