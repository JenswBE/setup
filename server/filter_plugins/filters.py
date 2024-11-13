#!/usr/bin/python3

class FilterModule(object):
    def filters(self):
        return {
            'to_caddy_headers': self.to_caddy_headers,
        }
    
    def remove_newlines(self, input):
        return input.replace("\\n", "")

    def to_caddy_headers(self, headers, directive="header"):
        header_list = [f"{directive} {header} `{self.remove_newlines(value)}`" for header, value in dict(headers).items()]
        return "\n".join(header_list)

