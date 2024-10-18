#!/usr/bin/python

import toml
import json

class FilterModule(object):

    def filters(self):
        return {
            'to_toml': self.to_toml,
        }

    # Based on https://www.iops.tech/blog/generate-toml-using-ansible-template/
    def to_toml(self, input):
        s = json.dumps(dict(input))
        d = json.loads(s)
        return toml.dumps(d)
