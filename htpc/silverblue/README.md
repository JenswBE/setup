# Fedora Silverblue 37

1. Enable SSH in Settings => Sharing => Remote Login
2. Copy SSH ID: `ssh-copy-id rango.jensw.eu`
3. Run ansible: `ansible-playbook main.yml`
4. Execute following commands:

```bash
sudo rpm-ostree override remove firefox firefox-langpacks
```

5. Reboot

## Known issues

- Input Remapper missing (see Fedora instructions)
- Seahorse missing (see Fedora instructions)

## Thanks to

- Inspiration on how to use Ansible Flatpak modules: https://github.com/j1mc/ansible-silverblue
