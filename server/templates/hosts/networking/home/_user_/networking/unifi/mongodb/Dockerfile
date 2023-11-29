FROM docker.io/library/mongo:4.4

# Unfortunately, the original Mongo image doesn't allow setting
# an UID and GID. Therefore, adding file with correct
# permissions using this workaround.
COPY mongo-init.js /docker-entrypoint-initdb.d/mongo-init.js
RUN chown mongodb /docker-entrypoint-initdb.d/mongo-init.js
