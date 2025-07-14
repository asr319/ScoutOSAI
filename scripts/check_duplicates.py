import os
import hashlib

def hash_file(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def scan(root):
    hashes = {}
    for dirpath, _, filenames in os.walk(root):
        if 'node_modules' in dirpath or '.pnpm' in dirpath:
            continue
        for name in filenames:
            if name.endswith(('.py', '.js', '.ts', '.json', '.yml', '.yaml')):
                if name == '__init__.py':
                    continue
                p = os.path.join(dirpath, name)
                h = hash_file(p)
                if h in hashes:
                    print(f"Duplicate file: {p} and {hashes[h]}")
                else:
                    hashes[h] = p

if __name__ == '__main__':
    scan('.')
