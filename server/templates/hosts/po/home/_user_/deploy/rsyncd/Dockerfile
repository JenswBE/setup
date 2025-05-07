FROM quay.io/panubo/sshd:latest

# Add dependencies
RUN apk add rrsync

# Setup SSH users
ARG SSH_USERS
ENV SSH_USERS=$SSH_USERS
COPY authorized_keys /keys_to_authorize
COPY setup.sh /setup.sh
COPY fix-perms.sh /etc/entrypoint.d/fix-perms.sh
RUN /usr/bin/env bash /setup.sh
