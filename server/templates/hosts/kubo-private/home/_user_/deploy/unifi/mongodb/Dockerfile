FROM docker.io/library/mongo:8.2

# Unfortunately, the original Mongo image doesn't allow setting
# an UID and GID. Therefore, adding file with correct
# permissions using this workaround.
COPY --chown=mongodb mongo-init.sh /docker-entrypoint-initdb.d/mongo-init.sh
