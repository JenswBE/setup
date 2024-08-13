# Keep version aligned with .github/workflows/test.yml
FROM docker.io/library/golang:1.23 AS builder
WORKDIR /src/
COPY main.go main.go
COPY go.mod go.mod
ARG TARGETOS TARGETARCH TARGETVARIANT
RUN --mount=type=cache,target=/root/.cache/go-build \
    --mount=type=cache,target=/go/pkg \
    CGO_ENABLED=0 GOOS=$TARGETOS GOARCH=$TARGETARCH GOARM=${TARGETVARIANT#v} go build -ldflags='-extldflags=-static' -o /bin/network-performance-file-generator ./...

FROM scratch
COPY --from=builder /bin/network-performance-file-generator /network-performance-file-generator
EXPOSE 8080
ENTRYPOINT ["/network-performance-file-generator"]
HEALTHCHECK CMD /network-performance-file-generator --healthcheck
