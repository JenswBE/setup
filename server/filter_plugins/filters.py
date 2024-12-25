#!/usr/bin/python3

import socket

from ansible.errors import AnsibleError
from ansible.module_utils.common.text.converters import to_native

class FilterModule(object):
    def filters(self):
        return {
            'enrich_hostnames': self.enrich_hostnames,
            'to_caddy_header_values': self.to_caddy_header_values,
        }
    
    def enrich_hostnames(self, input):
        result = {}
        for ip_type, hostnames in input.items():
            type_result = {}
            for hostname, data in hostnames.items():
                host_result = data
                fqdn = data["fqdn"]
                try:
                    host_result["ipv4"] = socket.gethostbyname(fqdn)
                except Exception as e:
                    raise AnsibleError(f"Failed to lookup IPv4 for FQDN '{fqdn}': {to_native(e)}")
                
                if data["ipv6"]:
                    try:
                        (_, _, _, _, sockaddr) = socket.getaddrinfo(fqdn, None, socket.AF_INET6)[0]
                        host_result["ipv6"] = sockaddr[0]
                    except Exception as e:
                        raise AnsibleError(f"Failed to lookup IPv6 for FQDN '{fqdn}': {to_native(e)}")
                else:
                    del(data["ipv6"]) # Ensures an error is thrown when trying to use "ipv6" in templates
                
                type_result[hostname] = host_result
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
