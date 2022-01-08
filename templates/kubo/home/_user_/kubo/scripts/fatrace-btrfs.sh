set -euo pipefail
fatrace --filter=OC --current-mount | ts '%Y-%m-%d %H:%M:%S -_-'