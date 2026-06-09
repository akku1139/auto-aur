#!/usr/bin/env python3
import json
import sys
from collections import deque
from common import get_deps, is_local_package, is_custom_patch, get_current_version, is_in_repositories

def main():
    if len(sys.argv) != 3:
        print("Usage: update_lock.py packages.txt lock.json")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        seeds = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    all_pkgs = set(seeds)
    frontier = list(seeds)
    while frontier:
        pkg = frontier.pop()
        deps = get_deps(pkg)
        new_deps = deps - all_pkgs
        all_pkgs.update(new_deps)
        frontier.extend(new_deps)

    graph = {pkg: get_deps(pkg) & all_pkgs for pkg in all_pkgs}

    in_degree = {pkg: 0 for pkg in all_pkgs}
    for deps in graph.values():
        for dep in deps:
            in_degree[dep] += 1

    q = deque([pkg for pkg in all_pkgs if in_degree[pkg] == 0])
    order = []
    while q:
        pkg = q.popleft()
        order.append(pkg)
        for dependant, deps in graph.items():
            if pkg in deps:
                in_degree[dependant] -= 1
                if in_degree[dependant] == 0:
                    q.append(dependant)

    if len(order) != len(all_pkgs):
        cyclic = all_pkgs - set(order)
        print(f"Error: Circular dependencies detected: {cyclic}", file=sys.stderr)
        # 循環に関係するサブグラフを表示
        subgraph = {pkg: graph[pkg] for pkg in cyclic if pkg in graph}
        print("Dependency subgraph causing cycle:", file=sys.stderr)
        for pkg, deps in subgraph.items():
            print(f"  {pkg} -> {deps}", file=sys.stderr)
        # さらに、各パッケージの公式リポジトリ有無を確認
        for pkg in cyclic:
            in_repo = is_in_repositories(pkg)
            print(f"  {pkg} in repositories: {in_repo}", file=sys.stderr)
        sys.exit(1)

    lock = {
        "version": 1,
        "packages": [],
        "build_order": order
    }
    for pkg in order:
        lock["packages"].append({
            "name": pkg,
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
