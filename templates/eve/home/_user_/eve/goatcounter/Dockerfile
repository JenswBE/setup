FROM alpine:latest as builder

ARG version

RUN wget "https://github.com/arp242/goatcounter/releases/download/${version}/goatcounter-dev-linux-amd64.gz" -O goatcounter.gz
RUN gunzip goatcounter.gz
RUN chmod +x goatcounter

FROM alpine:latest
RUN mkdir /db
COPY --from=builder goatcounter /usr/local/bin/goatcounter
EXPOSE 80
ENTRYPOINT [ "goatcounter" ]
CMD [ "serve", "-db", "sqlite+/db/goatcounter.sqlite3", "-listen", ":80", "-tls", "http", "-automigrate", "-email-from", "{{ ansible_hostname }}.goatcounter@{{ general_domain_default }}" ]