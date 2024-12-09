#!/usr/bin/python3

import socket

from ansible.errors import AnsibleError
from ansible.module_utils.common.text.converters import to_native

class FilterModule(object):
    def filters(self):
        return {
            'hostnames_to_ips': self.hostnames_to_ips,
            'to_caddy_header_values': self.to_caddy_header_values,
        }
    
    def hostnames_to_ips(self, input):
        result = {}
        for ip_type, hostnames in input.items():
            type_result = {}
            for hostname, fqdn in hostnames.items():
                try:
                    type_result[hostname] = socket.gethostbyname(fqdn)
                except Exception as e:
                    raise AnsibleError(f"Failed to lookup FQDN '{fqdn}': {to_native(e)}")
            result[ip_type] = type_result
        return result

    
    def remove_newlines(self, input):
        return input.replace("\\n", "")

    def to_caddy_header_values(self, headers, action):
        match action:
            case "replace":
                prefix_sign = ""
            case "default":
                prefix_sign = "?"
            case _:
                raise AnsibleError(f"Param action is missing or has an unsupported value")
        header_list = [f"{prefix_sign}{header} `{self.remove_newlines(value)}`" for header, value in dict(headers).items()]
        return "\n".join(header_list)
