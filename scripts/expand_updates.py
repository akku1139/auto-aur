#!/usr/bin/env python3
import json
import sys

def main():
    if len(sys.argv) != 4:
        print("Usage: expand_updates.py lock.json mapping.json final_build_list.txt")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        lock = json.load(f)
    with open(sys.argv[2]) as f:
        mapping = json.load(f)

    to_build = set()
    for pkg_info in lock["packages"]:
        name = pkg_info["name"]
        is_local = pkg_info.get("local", False)
        is_custom = pkg_info.get("custom", False)
        locked_version = pkg_info.get("version", "")

        # マッピングに登録されているか
        mapped = mapping.get("packages", {}).get(name)

        # ローカルまたはカスタムパッケージ
        if is_local or is_custom:
            # マッピングに存在しなければビルド
            if not mapped:
                to_build.add(name)
                continue
            built_version = mapped.get("version", "")
            if built_version != locked_version:
                to_build.add(name)
            # バージョンが同じでも、強制的にビルドしたい場合はここで追加（任意）
            # else: to_build.add(name)  # 常にビルド
            continue

        # 通常のAURパッケージ
        if not mapped:
            to_build.add(name)
            continue
        built_version = mapped.get("version", "")
        if built_version != locked_version:
            to_build.add(name)

    # 逆依存グラフで依存元も追加
    rev_deps = {pkg["name"]: set() for pkg in lock["packages"]}
    for pkg in lock["packages"]:
        for dep in pkg["deps"]:
            rev_deps[dep].add(pkg["name"])

    frontier = list(to_build)
    while frontier:
        pkg = frontier.pop()
        for depender in rev_deps.get(pkg, []):
            if depender not in to_build:
                to_build.add(depender)
                frontier.append(depender)

    with open(sys.argv[3], 'w') as f:
        for pkg in sorted(to_build):
            f.write(pkg + "\n")

if __name__ == '__main__':
    main()
