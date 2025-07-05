# Set env vars
APPDATA_DIR=/opt/appdata

# Helpers
borgmatic_mount() {
  REPO_NAME=${1:?}
  BACKUP_PATH=${2:?}
  echo "Mounting borg repo \"${REPO_NAME:?}\" with path \"${BACKUP_PATH:?}\" ..."
  sudo docker exec borgmatic mkdir -p /mnt/borg
  sudo docker exec borgmatic borgmatic --verbosity '-1' mount --repository ${REPO_NAME:?} --archive latest --mount-point /mnt/borg --path mnt/source/${REPO_NAME:?}/${BACKUP_PATH:?}
}

borgmatic_umount() {
  echo "Unmounting borg repo ..."
  sudo docker exec borgmatic mkdir -p /mnt/borg
  sudo docker exec borgmatic borgmatic --verbosity '-1' umount --mount-point /mnt/borg
}

compare_actual_backup_flat()
{
  # Params
  ACTUAL_CONTAINER=${1:?}
  ACTUAL_PATH=${2:?}
  BACKUP_APP=${3:?}
  BACKUP_PATH=${4:?}

  # Mount repo
  borgmatic_mount ${BACKUP_APP:?} "${BACKUP_PATH:?}"

  # Compare 3 newest files
  echo "Finding 3 newest files in source \"${ACTUAL_PATH:?}\" ..."
  sudo docker exec ${ACTUAL_CONTAINER:?} ls -Alt ${ACTUAL_PATH:?} | head -n 4
  echo "Finding 3 newest files in backup \"${BACKUP_APP:?}/${BACKUP_PATH:?}\" ..."
  sudo docker exec borgmatic ls -Alt "/mnt/borg/mnt/source/${BACKUP_APP:?}/${BACKUP_PATH:?}" | head -n 4

  # Unmount repo
  borgmatic_umount
}

compare_actual_backup_recursive()
{
  # Params
  ACTUAL_CONTAINER=${1:?}
  ACTUAL_PATH=${2:?}
  BACKUP_APP=${3:?}
  BACKUP_PATH=${4:?}

  # Mount repo
  borgmatic_mount ${BACKUP_APP:?} "${BACKUP_PATH:?}"

  # List size and change date of 3 newest files before today
  # Since Borgmatic uses BusyBox which doesn't support "newermt", we calculate the minutes since midnight locally.
  # This ensures a correct comparison. Based on https://stackoverflow.com/a/30374251
  MINS_SINCE_MIDNIGHT=$(( $(date "+10#%H * 60 + 10#%M") ))
  EXTRACT_PRINT_LAST_3='sort -nr | head -n 3 | cut -d" " -f2- | tr \\\n \\\0 | xargs -0 ls -lah'
  echo "Finding 3 newest files in source \"${ACTUAL_PATH:?}\" ..."
  sudo docker exec ${ACTUAL_CONTAINER:?} sh -c "find ${ACTUAL_PATH:?} -type f -mmin +${MINS_SINCE_MIDNIGHT:?} -exec stat -c '%Y %n' {} \; | ${EXTRACT_PRINT_LAST_3:?}"
  echo "Finding 3 newest files in backup \"${BACKUP_APP:?}/${BACKUP_PATH:?}\" ..."
  sudo docker exec borgmatic sh -c "find /mnt/borg/mnt/source/${BACKUP_APP:?}/${BACKUP_PATH:?} -type f -mmin +${MINS_SINCE_MIDNIGHT:?} -exec stat -c '%Y %n' {} \; | ${EXTRACT_PRINT_LAST_3:?}"

  # Unmount repo
  borgmatic_umount
}

validate_postgres()
{
  # Params
  BACKUP_APP=${1:?}
  BACKUP_PATH=${2:?}

  # Mount repo
  borgmatic_mount ${BACKUP_APP:?} ${BACKUP_PATH:?}

  # Copy all Postgres dumps to the restore point
  BACKUP_DIR="/mnt/borg/mnt/source/${BACKUP_APP:?}/${BACKUP_PATH:?}/*"
  RESTORE_DIR=/mnt/restore
  sudo docker exec borgmatic sh -c "rm -rf ${RESTORE_DIR:?}/*"
  echo "Copy dumps from \"${BACKUP_DIR:?}\" to \"/mnt/restore\" ..."
  sudo docker exec borgmatic sh -c "cp ${BACKUP_DIR:?} ${RESTORE_DIR:?}"

  # Check if backup files is correctly created
  echo "Validating dumps ..."
  sudo docker run --pull always --rm -v ${APPDATA_DIR:?}/borgmatic/borgmatic/restore:/backup postgres:alpine bash -c 'for f in /backup/*.pg_dump; do echo $f; pg_restore --list $f | head -n 12; echo; done;'
  sudo docker run --pull always --rm -v ${APPDATA_DIR:?}/borgmatic/borgmatic/restore:/backup postgres:alpine bash -c 'for f in /backup/*.pg_dumpall; do echo $f; head -n4 $f; echo; done;'

  # Unmount repo
  borgmatic_umount
}
