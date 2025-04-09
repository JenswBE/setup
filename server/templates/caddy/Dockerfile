FROM docker.io/library/caddy:2-builder AS builder
# Temporary locking caddy-security to v1.1.29 as higher versions require Go 1.24.
# See https://github.com/caddyserver/caddy-docker/issues/395
RUN xcaddy build --with github.com/caddy-dns/desec \
                 --with github.com/greenpau/caddy-security@v1.1.29  \
                 --with github.com/mholt/caddy-l4

FROM docker.io/library/caddy:2
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
