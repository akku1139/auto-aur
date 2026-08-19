#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def read_filter(path):
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None
    lines = [line.strip() for line in p.read_text().splitlines()
             if line.strip() and not line.startswith('#')]
    return set(lines) if lines else None

def main():
    if len(sys.argv) not in (4, 5):
        print("Usage: expand_updates.py lock.json mapping.json final_build_list.txt [package_filter.txt]")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        lock = json.load(f)
    with open(sys.argv[2]) as f:
        mapping = json.load(f)

    pkg_infos = {pkg["name"]: pkg for pkg in lock["packages"]}
    all_pkg_names = set(pkg_infos.keys())
    deps_map = {pkg["name"]: set(pkg.get("deps", [])) for pkg in lock["packages"]}

    changed = set()
    for name, info in pkg_infos.items():
        mapped = mapping.get("packages", {}).get(name)
        locked_version = info.get("version", "")
        locked_vcs_ref = info.get("vcs_ref")
        if not mapped:
            changed.add(name)
            continue
        if mapped.get("version", "") != locked_version:
            changed.add(name)
            continue
        if locked_vcs_ref and mapped.get("vcs_ref") != locked_vcs_ref:
            changed.add(name)

    requested_filter = read_filter(sys.argv[4] if len(sys.argv) == 5 else None)

    if requested_filter is not None:
        missing = requested_filter - all_pkg_names
        if missing:
            print(f"Error: requested packages not found in lock: {sorted(missing)}", file=sys.stderr)
            sys.exit(1)

        closure = set()
        stack = list(requested_filter)
        while stack:
            pkg = stack.pop()
            if pkg in closure:
                continue
            closure.add(pkg)
            for dep in deps_map.get(pkg, set()):
                if dep in all_pkg_names and dep not in closure:
                    stack.append(dep)

        rev = {pkg: set() for pkg in closure}
        for pkg in closure:
            for dep in deps_map[pkg]:
                if dep in closure:
                    rev[dep].add(pkg)

        affected = set(changed & closure)
        frontier = list(affected)
        while frontier:
            pkg = frontier.pop()
            for depender in rev.get(pkg, []):
                if depender in closure and depender not in affected:
                    affected.add(depender)
                    frontier.append(depender)

        to_build = affected | requested_filter
    else:
        rev = {pkg: set() for pkg in all_pkg_names}
        for pkg in all_pkg_names:
            for dep in deps_map[pkg]:
                if dep in all_pkg_names:
                    rev[dep].add(pkg)

        to_build = set(changed)
        frontier = list(to_build)
        while frontier:
            pkg = frontier.pop()
            for depender in rev.get(pkg, []):
                if depender not in to_build:
                    to_build.add(depender)
                    frontier.append(depender)

    with open(sys.argv[3], 'w') as f:
        for pkg in sorted(to_build):
            f.write(pkg + "\n")

if __name__ == '__main__':
    main()
