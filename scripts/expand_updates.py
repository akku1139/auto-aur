#!/usr/bin/env python3
import json
import sys
from common import get_current_version

def main():
    if len(sys.argv) != 4:
        print("Usage: expand_updates.py lock.json mapping.json final_build_list.txt")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        lock = json.load(f)
    with open(sys.argv[2]) as f:
        mapping = json.load(f)

    # ビルドが必要なパッケージを特定（mapping にない または バージョン不一致）
    to_build = set()
    for pkg_info in lock["packages"]:
        name = pkg_info["name"]
        # ローカルパッケージやカスタムパッチは常にビルド（必要に応じて調整）
        if pkg_info.get("local") or pkg_info.get("custom"):
            # この例ではビルド対象に含めない（必要ならコメントアウト）
            continue
        locked_version = pkg_info.get("version", "")
        # mapping に存在しない → 未ビルド
        if name not in mapping.get("packages", {}):
            to_build.add(name)
            continue
        # AUR の最新バージョンを取得
        current_version = get_current_version(name)
        if current_version != locked_version:
            to_build.add(name)

    # 逆依存グラフを構築
    rev_deps = {pkg["name"]: set() for pkg in lock["packages"]}
    for pkg in lock["packages"]:
        for dep in pkg["deps"]:
            rev_deps[dep].add(pkg["name"])

    # ビルド対象 + それに依存する全パッケージを収集
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
