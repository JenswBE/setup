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

## Generate rclone password

```bash
rclone obscure <PASS>
```

## Generate new ed25519 SSH key for Borgmatic

```bash
ssh-keygen -t ed25519 -N '' -f borgmatic
```
