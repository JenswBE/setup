# Personal Ansible Stuff

As a failsafe, it's mandatory to use `--limit` option.
Without this option, the playbook will fail.

```bash
# Run complete setup for a host
ansible-playbook main.yml --ask-vault-pass --ask-become-pass --limit <HOSTNAME>

# To only run config steps
ansible-playbook main.yml --ask-vault-pass --ask-become-pass --skip-tags setup --limit <HOSTNAME>
```