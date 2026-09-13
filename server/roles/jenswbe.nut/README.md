# NUT / UPS

To configure the `battery.charge.low` setting, execute:

```bash
# Print current value
upsc apc battery.charge.low

# Update value to 30%
# The user creds are based on /etc/nut/upsd.users
upsrw -s battery.charge.low=30 -u fiona apc
```
