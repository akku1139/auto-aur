#!/usr/bin/env python3
import os
import shutil
import sys

def main():
    if len(sys.argv) != 4:
        print("Usage: collect_built.py source_dir target_dir build_list.txt")
        sys.exit(1)
    src = sys.argv[1]
    dst = sys.argv[2]
    with open(sys.argv[3]) as f:
        needed = set(line.strip() for line in f if line.strip())

    os.makedirs(dst, exist_ok=True)
    for fname in os.listdir(src):
        if not fname.endswith('.pkg.tar.zst'):
            continue
        # 簡易パッケージ名抽出 (最初の '-' まで、ただしパッケージ名に '-' を含む場合は不完全)
        pkgname = fname.split('-')[0]
        if pkgname in needed:
            shutil.copy(os.path.join(src, fname), os.path.join(dst, fname))

if __name__ == '__main__':
    main()
