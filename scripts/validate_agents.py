import os

REQUIRED_LINE = 'All CI/CD, security, and agent checks passed.'


def check_agents(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if REQUIRED_LINE not in content:
        print(f"{path} missing policy line")
        return False
    return True


def main():
    success = True
    for root, _, files in os.walk('.'):
        for name in files:
            if name == 'AGENTS.md':
                if not check_agents(os.path.join(root, name)):
                    success = False
    if not success:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
