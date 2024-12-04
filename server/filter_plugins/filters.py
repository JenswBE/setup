#!/usr/bin/python3

import socket

from ansible.errors import AnsibleError
from ansible.module_utils.common.text.converters import to_native

class FilterModule(object):
    def filters(self):
        return {
            'hostnames_to_ips': self.hostnames_to_ips,
            'to_caddy_headers': self.to_caddy_headers,
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

    def to_caddy_headers(self, headers, directive="header"):
        header_list = [f"{directive} {header} `{self.remove_newlines(value)}`" for header, value in dict(headers).items()]
        return "\n".join(header_list)
