# How-to

## Install secrets

Run from this folder:

```bash
git clone git@github.com:JenswBE/setup-vars.git ../../../setup-vars
cd ../../../setup-vars
SECRETS_DIR="$(pwd)"
cd -
ln -snf "${SECRETS_DIR:?}/server" secret
```

## Generate Treafik basic auth credentials

```bash
htpasswd -nBC 10 <USERNAME>
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
