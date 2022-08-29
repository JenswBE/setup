import json
import sys

ports = json.loads(sys.argv[1])
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
print(json.dumps(output))
