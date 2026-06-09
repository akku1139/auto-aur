#!/usr/bin/env python3
import json
import sys
from collections import deque
from common import (
    get_deps, is_local_package, is_custom_patch, get_current_version,
    preload_aur_cache, get_aur_pkgbase
)

def main():
    if len(sys.argv) != 3:
        print("Usage: update_lock.py packages.txt lock.json")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        seeds = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    # Step 1: Collect all dependencies
    all_pkgs = set(seeds)
    frontier = list(seeds)
    while frontier:
        pkg = frontier.pop()
        deps = get_deps(pkg)
        new_deps = deps - all_pkgs
        all_pkgs.update(new_deps)
        frontier.extend(new_deps)

    # Step 2: Preload AUR info for performance
    aur_pkgs = [pkg for pkg in all_pkgs if not (is_local_package(pkg) or is_custom_patch(pkg))]
    if aur_pkgs:
        print(f"Preloading AUR info for {len(aur_pkgs)} packages...", file=sys.stderr)
        preload_aur_cache(aur_pkgs)

    # Step 3: Build dependency graph (pkg -> deps)
    graph = {pkg: get_deps(pkg) & all_pkgs for pkg in all_pkgs}

    # Step 4: Compute in-degree (number of packages that depend on this package)
    in_degree = {pkg: 0 for pkg in all_pkgs}
    for deps in graph.values():
        for dep in deps:
            in_degree[dep] += 1

    # Step 5: Topological sort (Kahn's algorithm)
    q = deque([pkg for pkg in all_pkgs if in_degree[pkg] == 0])
    order = []
    while q:
        pkg = q.popleft()
        order.append(pkg)
        for dep in graph[pkg]:
            in_degree[dep] -= 1
            if in_degree[dep] == 0:
                q.append(dep)

    if len(order) != len(all_pkgs):
        cyclic = all_pkgs - set(order)
        print(f"Error: Circular dependencies detected: {cyclic}", file=sys.stderr)
        print("Full dependency graph:", file=sys.stderr)
        for pkg in sorted(all_pkgs):
            deps = graph[pkg]
            print(f"  {pkg} -> {deps}", file=sys.stderr)
        print("In-degree after processing:", file=sys.stderr)
        for pkg in sorted(all_pkgs):
            print(f"  {pkg}: {in_degree.get(pkg, '?')}", file=sys.stderr)
        sys.exit(1)

    # 正しいビルド順にするため逆順に並べ替え（依存するものが先に来る）
    order.reverse()

    # Step 6: Generate lock.json
    lock = {
        "version": 1,
        "packages": [],
        "build_order": order
    }
    for pkg in order:
        pkgbase = pkg
        if not (is_local_package(pkg) or is_custom_patch(pkg)):
            # AUR パッケージの場合、実際の pkgbase を取得
            try:
                pkgbase = get_aur_pkgbase(pkg)
            except:
                # フォールバック: pkg をそのまま使う
                pass
        lock["packages"].append({
            "name": pkg,
            "pkgbase": pkgbase,
            "version": get_current_version(pkg),
            "deps": list(graph[pkg]),
            "build_order": order.index(pkg),
            "local": is_local_package(pkg),
            "custom": is_custom_patch(pkg)
        })

    with open(sys.argv[2], 'w') as f:
        json.dump(lock, f, indent=2)

if __name__ == '__main__':
    main()
