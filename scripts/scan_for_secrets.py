import os
import re

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|password)[\"']?\s*[:=]\s*[\"'][^\"']{8,}[\"']"),
    re.compile(r"AIza[0-9A-Za-z-_]{35}"),  # Example Google API Key pattern
    # Add more patterns as needed!
]

def scan_file(filepath: str) -> None:
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            for pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    print(f"Potential secret in {filepath} at line {i}: {line.strip()}")

def scan_repo(root_dir: str) -> None:
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.endswith(('.py', '.js', '.ts', '.env', '.yml', '.yaml', '.json', '.md')):
                scan_file(os.path.join(dirpath, fname))

if __name__ == "__main__":
    scan_repo(".")
