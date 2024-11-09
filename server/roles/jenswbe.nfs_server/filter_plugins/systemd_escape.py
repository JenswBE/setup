# https://gist.github.com/Zocker1999NET/985a94c74d6f746efc5e0fbb22bff206
# Copyright (C) 2020 Felix Stupp
# Licensed under MIT
# place beside your playbook into filter_plugins/ to use in ansible

from functools import partial
import re
import subprocess
import sys

from ansible.errors import AnsibleFilterError

def systemd_escape(text, instance=False, mangle=False, path=False, suffix=None, template=None, unescape=False):
    options_map = {
        "instance": instance,
        "mangle": mangle,
        "path": path,
        "unescape": unescape,
    }
    args_map = {
        "suffix": suffix,
        "template": template,
    }
    args = ["/usr/bin/env", "systemd-escape"] + [f"--{name}" for name, val in options_map.items() if val] + [f"--{name}={val}" for name, val in args_map.items() if val is not None] + [text]
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        raise AnsibleFilterError(re.sub('\u001b\\[.*?[@-~]', '', result.stderr.rstrip('\n')))
    return result.stdout.rstrip('\n')

class FilterModule(object):
    def filters(self):
        return {
            'systemd_escape': systemd_escape,
            'systemd_escape_mount': partial(systemd_escape, path=True, suffix='mount')
        }

if __name__ == '__main__':
    print(systemd_escape(sys.argv[1]))
