#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mapping', required=True)
    parser.add_argument('--new-packages', required=True)
    parser.add_argument('--release-tag', required=True)
    parser.add_argument('--db-output', required=True)
    parser.add_argument('--redirects', required=True)
    args = parser.parse_args()

    # 1. mapping.json 読み込み
    with open(args.mapping) as f:
        mapping = json.load(f)

    # 2. 新しいパッケージでマッピング更新
    for pkg_file in Path(args.new_packages).glob('*.pkg.tar.zst'):
        fname = pkg_file.name
        pkgname = fname.split('-')[0]  # 簡易抽出
        mapping['packages'][pkgname] = {
            "filename": fname,
            "release_tag": args.release_tag
        }

    # 3. データベース再生成
    db_dir = Path(args.db_output).parent
    db_dir.mkdir(parents=True, exist_ok=True)
    temp_dir = Path('/tmp/repo_build')
    temp_dir.mkdir(exist_ok=True)

    # 前回のDBがあればコピー
    old_db = Path(args.db_output)
    if old_db.exists():
        shutil.copy(old_db, temp_dir / 'auto-aur.db.tar.gz')

    # 今回の新パッケージを追加 (古いパッケージファイルはダウンロードしない)
    new_pkgs = list(Path(args.new_packages).glob('*.pkg.tar.zst'))
    if (temp_dir / 'auto-aur.db.tar.gz').exists():
        subprocess.run(['repo-add', temp_dir / 'auto-aur.db.tar.gz'] + new_pkgs, check=True)
    else:
        subprocess.run(['repo-add', temp_dir / 'auto-aur.db.tar.gz'] + new_pkgs, check=True)

    shutil.copy(temp_dir / 'auto-aur.db.tar.gz', old_db)

    # 4. _redirects 生成
    repo = os.environ['GITHUB_REPOSITORY']
    lines = []
    for pkgname, info in mapping['packages'].items():
        filename = info['filename']
        tag = info['release_tag']
        src = f"/pool/{filename}"
        target = f"https://github.com/{repo}/releases/download/{tag}/{filename}"
        lines.append(f"{src} {target} 302")
    with open(args.redirects, 'w') as f:
        f.write("\n".join(lines))

    # 更新したmappingを保存
    with open(args.mapping, 'w') as f:
        json.dump(mapping, f, indent=2)

if __name__ == '__main__':
    main()
