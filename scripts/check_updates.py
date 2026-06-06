#!/usr/bin/env python3
import json
import sys
from common import get_current_version

def main():
    if len(sys.argv) != 2:
        print("Usage: check_updates.py lock.json")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        lock = json.load(f)

    for pkg_info in lock["packages"]:
        if pkg_info.get("local") or pkg_info.get("custom"):
            continue
        name = pkg_info["name"]
        current = get_current_version(name)
        locked = pkg_info.get("version", "")
        if current != locked:
            print(name)

if __name__ == '__main__':
    main()
