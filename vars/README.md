# How-to

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
