# Ansible
Personal Ansible Stuff

By default, the tasks will run against `localhost:2222`.
You can run a VM on this address to perform test runs.
To target a real you'll have to use the inventory name explicitely.

```bash
# Run complete setup for a host
ansible-playbook main.yml --ask-vault-pass --ask-become-pass --limit <HOSTNAME>

# To only run config steps
ansible-playbook main.yml --ask-vault-pass --ask-become-pass --skip-tags setup --limit <HOSTNAME>
```