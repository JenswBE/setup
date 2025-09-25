# NBDE client

## Warning

Seems DNS isn't available in Debian in the init when clevis tries to unlock the drive.
Therefore, hostnames won't work. Use a static IP instead for the tang server!

For more info, see:
- https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1005963
- https://github.com/latchset/clevis/issues/413

## Instructions

**Note:** This role is only for root devices. See role `jenswbe.luks_decrypt` for non-root devices.

```bash
# Use single Tang server
sudo clevis luks bind -d ${LUKS_DEVICE:?} tang '{"url": "http://{{ ip['kubo'] }}:7500"}'

# Use multiple Tang servers
sudo clevis luks bind -d ${LUKS_DEVICE:?} sss '{"t":1,"pins":{"tang":[{"url":"http://{{ ip['kubo'] }}:7500"},{"url":"http://{{ ip['fiona'] }}:7500"}]}}'

# Manual install - Client - Debian/Ubuntu
sudo apt install clevis clevis-luks clevis-initramfs

# Manual install - Client - Fedora
sudo dnf install clevis clevis-luks clevis-dracut
sudo grubby --update-kernel=ALL --args="rd.neednet=1"
sudo dracut -fv --regenerate-all
```

See for more info
- [RedHat Clevis/Tang guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/security_hardening/configuring-automated-unlocking-of-encrypted-volumes-using-policy-based-decryption_security-hardening#configuring-manual-enrollment-of-volumes-using-clevis_configuring-automated-unlocking-of-encrypted-volumes-using-policy-based-decryption)
- [Ubuntu Clevis guide](https://semanticlab.net/sysadmin/encryption/Network-bound-disk-encryption-in-ubuntu-20.04/)
