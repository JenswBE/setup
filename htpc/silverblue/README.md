# Fedora Silverblue 37

1. Enable SSH in Settings => Sharing => Remote Login
2. Copy SSH ID: `ssh-copy-id rango.jensw.lan`
3. Run ansible: `ansible-playbook --ask-become-pass main.yml`

## Known issues

- Input Remapper missing (see Fedora instructions)
- Seahorse missing (see Fedora instructions)

## Thanks to

- Inspiration on how to use Ansible Flatpak modules: https://github.com/j1mc/ansible-silverblue
