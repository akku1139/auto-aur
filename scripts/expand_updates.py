#!/usr/bin/env python3
import json
import sys

def main():
    if len(sys.argv) != 4:
        print("Usage: expand_updates.py lock.json update_list.txt final_build_list.txt")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        lock = json.load(f)

    with open(sys.argv[2]) as f:
        updates = set(line.strip() for line in f if line.strip())

    # 逆依存グラフ構築
    rev_deps = {pkg["name"]: set() for pkg in lock["packages"]}
    for pkg in lock["packages"]:
        for dep in pkg["deps"]:
            rev_deps[dep].add(pkg["name"])

    to_build = set(updates)
    frontier = list(updates)
    while frontier:
        pkg = frontier.pop()
        for depender in rev_deps.get(pkg, []):
            if depender not in to_build:
                to_build.add(depender)
                frontier.append(depender)

    with open(sys.argv[3], 'w') as f:
        for pkg in to_build:
            f.write(pkg + "\n")

if __name__ == '__main__':
    main()
