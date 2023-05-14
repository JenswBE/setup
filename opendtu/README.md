https://github.com/tbnobody/OpenDTU

```bash
sudo podman run --rm -t -i --privileged --device=/dev/ttyUSB0 \
    --name esptool -v /var/home/jens/Downloads/:/Downloads:z docker.io/library/python:3 /bin/bash
pip install esptool
# Follow GitHub instructions
```
