import sys

path = 'CHANGELOG.md'
try:
    with open(path) as f:
        lines = f.readlines()
except FileNotFoundError:
    print('Missing CHANGELOG.md')
    sys.exit(1)

if len(lines) < 2:
    print('CHANGELOG.md needs an entry')
    sys.exit(1)
