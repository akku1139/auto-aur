#!/usr/bin/env python3
import json
import sys
import os
from collections import deque
from common import (
    get_deps, is_local_package, is_custom_patch, get_current_version,
    preload_aur_cache, get_aur_pkgbase
)

def main():
    if len(sys.argv) not in (3, 4):
        print("Usage: update_lock.py packages.txt lock.json [extra_packages.txt]")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        seeds = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    if len(sys.argv) == 4:
        extra_file = sys.argv[3]
        if os.path.exists(extra_file):
            with open(extra_file) as f:
                extra = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            seeds = list(dict.fromkeys(seeds + extra))

    all_pkgs = set(seeds)
    processed = set()

    while True:
        # 現在判明しているAURパッケージのうち、まだキャッシュに無いものを
        # まとめてAUR RPCで取得する
        aur_to_fetch = [
            pkg for pkg in all_pkgs
            if not (is_local_package(pkg) or is_custom_patch(pkg))
        ]
        if aur_to_fetch:
            print(f"Preloading AUR info for up to {len(aur_to_fetch)} packages...", file=sys.stderr)
            preload_aur_cache(aur_to_fetch)

        added_new = False
        for pkg in list(all_pkgs):
            if pkg in processed:
                continue
            deps = get_deps(pkg)          # キャッシュ済みなら高速
            for dep in deps:
                if dep not in all_pkgs:
                    all_pkgs.add(dep)
                    added_new = True
            processed.add(pkg)

        # 新しい依存が増えなければ終了
        if not added_new:
            break

    # ---- 以降は既存の処理 ----
    # Step 3: Build dependency graph (pkg -> deps)
    graph = {pkg: get_deps(pkg) & all_pkgs for pkg in all_pkgs}

    # Step 4: Compute in-degree
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
