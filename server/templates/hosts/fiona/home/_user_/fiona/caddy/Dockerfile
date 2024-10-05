FROM docker.io/library/caddy:2-builder AS builder
RUN xcaddy build --with github.com/caddy-dns/desec

FROM docker.io/library/caddy:2
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
