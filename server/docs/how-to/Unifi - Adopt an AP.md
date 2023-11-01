# How-to: Adopt a Unifi AP

1. Factory reset AP
2. Ensure computer is on same subnet
3. Login with SSH. If on Fedora, you might have to use `sudo update-crypto-policies --set LEGACY` as described by https://kcore.org/2023/03/27/ssh-unifi-fedora-37/.
4. Execute `set-inform http://CONTROLLER_HOSTNAME:8080/inform`
