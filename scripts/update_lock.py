#!/usr/bin/env python3
import json
import sys
from collections import deque
from common import get_deps, is_local_package, is_custom_patch, get_current_version, preload_aur_cache

def main():
    if len(sys.argv) != 3:
        print("Usage: update_lock.py packages.txt lock.json")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        seeds = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    # ステップ1: 全依存パッケージの収集
    all_pkgs = set(seeds)
    frontier = list(seeds)
    while frontier:
        pkg = frontier.pop()
        deps = get_deps(pkg)
        new_deps = deps - all_pkgs
        all_pkgs.update(new_deps)
        frontier.extend(new_deps)

    # ステップ2: AUR パッケージの情報を一括プリロード（パフォーマンス改善）
    aur_pkgs = [pkg for pkg in all_pkgs if not (is_local_package(pkg) or is_custom_patch(pkg))]
    if aur_pkgs:
        print(f"Preloading AUR info for {len(aur_pkgs)} packages...", file=sys.stderr)
        preload_aur_cache(aur_pkgs)

    # ステップ3: 依存グラフ構築
    graph = {}
    for pkg in all_pkgs:
        deps = get_deps(pkg)
        graph[pkg] = deps & all_pkgs

    # ステップ4: 次数計算とトポロジカルソート
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

    # 循環依存チェック
    if len(order) != len(all_pkgs):
        cyclic = all_pkgs - set(order)
        print(f"Error: Circular dependencies detected: {cyclic}", file=sys.stderr)
        # 詳細な依存関係を出力
        print("Full dependency graph:", file=sys.stderr)
        for pkg in sorted(all_pkgs):
            deps = graph[pkg]
            print(f"  {pkg} -> {deps}", file=sys.stderr)
        print("In-degree after processing:", file=sys.stderr)
        for pkg in sorted(all_pkgs):
            print(f"  {pkg}: {in_degree.get(pkg, '?')}", file=sys.stderr)
        sys.exit(1)

    # ステップ5: lock.json の生成
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
