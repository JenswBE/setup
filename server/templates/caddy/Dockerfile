FROM docker.io/library/caddy:2-builder AS builder
RUN xcaddy build --with github.com/caddy-dns/desec \
                 --with github.com/greenpau/caddy-security \
                 --with github.com/mholt/caddy-l4

FROM docker.io/library/caddy:2
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
