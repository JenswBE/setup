# How-to

## Install secrets

Run from this folder:

```bash
git clone git@github.com:JenswBE/setup-private.git ../../../setup-private
cd ../../../setup-private
SECRETS_DIR="$(pwd)"
cd -
ln -snf "${SECRETS_DIR:?}/vars/server" secret
```

## Generate random alphanumeric string

Based on https://unix.stackexchange.com/a/230676

```bash
tr -dc A-Za-z0-9 </dev/random | head -c 32; echo
```

## Generate Treafik basic auth credentials

```bash
podman run -it --rm docker.io/library/httpd:2-alpine htpasswd -nBC 10 <USERNAME>
```

## Generate rclone password

```bash
rclone obscure <PASS>
```

## Generate imgproxy key and salt

See https://docs.imgproxy.net/configuration?id=url-signature

```bash
echo $(xxd -g 2 -l 64 -p /dev/random | tr -d '\n')
```
