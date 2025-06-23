ARG GOATCOUNTER_IMAGE=docker.io/library/alpine:latest

FROM ${GOATCOUNTER_IMAGE} AS builder

ARG arch
ARG version

RUN wget "https://github.com/arp242/goatcounter/releases/download/${version:?}/goatcounter-${version:?}-linux-${arch:?}.gz" -O goatcounter.gz
RUN gunzip goatcounter.gz
RUN chmod +x goatcounter

FROM ${GOATCOUNTER_IMAGE}
RUN mkdir /db
COPY --from=builder goatcounter /usr/local/bin/goatcounter
EXPOSE 80
ENTRYPOINT [ "goatcounter" ]
CMD [ "serve", "-db", "sqlite+/db/goatcounter.sqlite3", "-listen", ":80", "-tls", "http", "-automigrate", "-email-from", "{{ inventory_hostname }}.goatcounter@{{ general_domain_default }}" ]
