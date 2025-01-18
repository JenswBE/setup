# Fedora Silverblue 41

1. Enable SSH in Settings => System => Secure Shell
2. Copy SSH ID: `ssh-copy-id htpc@rango.jensw.eu`
3. Ensure required collections are installed: `ansible-galaxy collection install --force -r requirements.yml`
4. Run ansible: `ansible-playbook htpc.yml --limit rango`
5. Execute following commands:

```bash
sudo rpm-ostree override remove firefox firefox-langpacks
```

5. Reboot
6. Execute following commands:

```bash
sudo systemctl enable --now input-remapper
```

7. Setup following remappings in input-remapper:

   - Caps Lock to Tab
   - Menu button to Right mouse click

## Thanks to

- Inspiration on how to use Ansible Flatpak modules: https://github.com/j1mc/ansible-silverblue
