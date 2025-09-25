#!/usr/bin/python3

import socket

from ansible.errors import AnsibleError
from ansible.module_utils.common.text.converters import to_native

class FilterModule(object):
    def filters(self):
        return {
            'enrich_hostnames': self.enrich_hostnames,
            'get_dict_key_contains': self.get_dict_key_contains,
            'group_names_to_zabbix_templates': self.group_names_to_zabbix_templates,
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

    def get_dict_key_contains(self, haystack_dict, needle_key):
        """This function searches for the first dict key in haystack_dict which contains needle_key"""
        found = []
        for k, v in haystack_dict.items():
            if needle_key in k:
                found.append(k)
                value = v

        match len(found):
            case 0:
                keys = sorted(haystack_dict.keys())
                raise AnsibleError(f"None of the keys contain '{needle_key}': {', '.join(keys)}")
            case 1:
                return value
            case _:
                raise AnsibleError(f"Multiple keys contain '{needle_key}': {', '.join(found)}")

    def group_names_to_zabbix_templates(self, group_names):
        # Settings
        templates = ["Linux by Zabbix agent"] # Default templates
        mapping = {
            "docker_host": ["Docker by Zabbix agent 2"],
            "zabbix_server": ["Zabbix server health"],
        }

        # Add templates
        for group_name, group_templates in mapping.items():
            if group_name in group_names:
                templates.extend(group_templates)
        return templates

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
