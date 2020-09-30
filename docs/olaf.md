# Olaf the Great NAS
Config for my home NAS

## After `docker-compose up -d`
### Borgmatic
1. Execute `docker exec -it borgmatic sh -c "ssh -p <PORT> <BORG_USER>@<BORG_HOST>"`, check and accept the host key
2. Execute `ssh-keygen` and create a new ssh key with blank passphrase in `conf/borgmatic/ssh`
3. Add public key to allowed ssh keys at remote host (depending on service)
4. Copy from template and edit `conf/borgmatic/borgmatic.d/config.yaml`
5. Change permissions with `chmod 600 config.yaml`
6. Init repo if required with `docker exec borgmatic sh -c "borgmatic --init --encryption repokey-blake2"`
7. Perform a backup to test the setup with `docker exec borgmatic sh -c "borgmatic --verbosity 1"`
8. Optional: Backup your repo key file with `docker exec borgmatic sh -c "BORG_RSH=\"ssh -i /root/.ssh/<NAME_OF_SSH_KEY>\" borg key export --qr-html <FULL_REPO_NAME> /root/.ssh/repokey.html"`. Your file is available at `conf/borgmatic/ssh/repokey.html`.

### Transmission
1. Set correct permission with `sudo chown 233:233 /media/data/services/transmission/`
2. Go through online settings
  - Category Torrents
    - Set "Download to" to `/downloads`
    - Set "Directory for incomplete files" to `/running`
    - Set "Stop seeding at ratio" to 3
  - Category Queue
    - Set "Download Queue Size" to 10

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

## Scheduled jobs
### One shot
- None

### Continuous
- Every 15 mins: Update IP in DNS (olaf-clc.yml => cloudflare-dyndns.timer)

### 01:00 Daily application jobs
- None

### 02:00 Prepare backup
- None

### 03:00 Perform backup
- Run Borgmatic (conf/borgmatic/borgmatic.d/crontab.txt)

### 04:00 Perform application updates
- Run Watchtower (docker-compose.yml)

### System tasks
- 05:00 Update and restart (unattended updates)
- 06:00 First of month: Scrub BTRFS filesystem (olaf-clc.yml => btrfs-scrub.timer)
