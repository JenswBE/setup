# Based on https://www.keycloak.org/server/containers

ARG KC_IMAGE=quay.io/keycloak/keycloak:18.0

FROM ${KC_IMAGE} as builder
ENV KC_DB=postgres
ENV KC_METRICS_ENABLED=false
RUN /opt/keycloak/bin/kc.sh build

FROM ${KC_IMAGE}
COPY --from=builder /opt/keycloak/lib/quarkus/ /opt/keycloak/lib/quarkus/
WORKDIR /opt/keycloak
ENTRYPOINT ["/opt/keycloak/bin/kc.sh", "start"]
