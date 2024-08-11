#!/usr/bin/python

import toml
import json

class FilterModule(object):

    def filters(self):
        return {
            'parse_ufw_firewall_ports': self.parse_ufw_firewall_ports,
            'to_toml': self.to_toml,
        }


    def parse_ufw_firewall_ports(self, ports):
        output = []
        for port in ports:
            for proto in port['protos']:
                for from_network in port['from_networks']:
                    output.append({
                        'comment': port['comment'],
                        'port': port['port'],
                        'proto': proto,
                        'from_network': from_network,
                    })
        return output

    # Based on https://www.iops.tech/blog/generate-toml-using-ansible-template/
    def to_toml(self, input):
        s = json.dumps(dict(input))
        d = json.loads(s)
        return toml.dumps(d)
