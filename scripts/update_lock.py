#!/usr/bin/env python3
import json
import sys
import os
from collections import deque
from common import (
    get_deps, is_local_package, is_custom_patch, get_current_version,
    preload_aur_cache, get_aur_pkgbase, parse_vcs_source, get_vcs_ref,
    fetch_aur_srcinfo
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

    missing_packages = set()

    all_pkgs = set(seeds)
    processed = set()

    def safe_get_deps(pkg):
        if pkg in missing_packages:
            return set()
        try:
            return get_deps(pkg)
        except ValueError as e:
            if 'not found in AUR' in str(e):
                missing_packages.add(pkg)
                return set()
            raise

    while True:
        aur_to_fetch = [
            pkg for pkg in all_pkgs
            if not (is_local_package(pkg) or is_custom_patch(pkg))
            and pkg not in missing_packages
        ]
        if aur_to_fetch:
            print(f"Preloading AUR info for up to {len(aur_to_fetch)} packages...", file=sys.stderr)
            preload_aur_cache(aur_to_fetch)

        added_new = False
        for pkg in list(all_pkgs):
            if pkg in processed or pkg in missing_packages:
                continue

            deps = safe_get_deps(pkg)
            if pkg in missing_packages:
                all_pkgs.discard(pkg)
                continue

            for dep in deps:
                if dep not in all_pkgs and dep not in missing_packages:
                    all_pkgs.add(dep)
                    added_new = True
            processed.add(pkg)

        if not added_new and not all_pkgs - processed:
            break

    if missing_packages:
        with open('missing_packages.txt', 'w') as f:
            for pkg in sorted(missing_packages):
                f.write(pkg + '\n')

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
        is_local = is_local_package(pkg)
        is_custom = is_custom_patch(pkg)
        if not (is_local or is_custom):
            # AUR パッケージの場合、実際の pkgbase を取得
            try:
                pkgbase = get_aur_pkgbase(pkg)
            except:
                # フォールバック: pkg をそのまま使う
                pass

        vcs_ref = None
        if is_local:
            srcinfo = get_local_srcinfo(pkg)
        elif is_custom:
            srcinfo = get_custom_srcinfo(pkg)
        else:
            if pkg.endswith('-git'):
                try:
                    srcinfo = fetch_aur_srcinfo(pkgbase)
                except Exception:
                    srcinfo = None
            else:
                srcinfo = None

        if srcinfo:
            parsed = parse_vcs_source(srcinfo)
            if parsed:
                url, frag = parsed
                if not frag.startswith('commit='):
                    ref = None
                    if frag.startswith('branch='):
                        ref = frag.split('=', 1)[1]
                    elif frag.startswith('tag='):
                        ref = 'refs/tags/' + frag.split('=', 1)[1]
                    head = get_vcs_ref(url, ref)
                    if head:
                        vcs_ref = head

        entry = {
            "name": pkg,
            "pkgbase": pkgbase,
            "version": get_current_version(pkg),
            "deps": list(graph[pkg]),
            "build_order": order.index(pkg),
            "local": is_local,
            "custom": is_custom,
        }
        if vcs_ref:
            entry["vcs_ref"] = vcs_ref
        lock["packages"].append(entry)

    with open(sys.argv[2], 'w') as f:
        json.dump(lock, f, indent=2)

if __name__ == '__main__':
    main()
