#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mapping', required=True)
    parser.add_argument('--new-packages', required=True)
    parser.add_argument('--release-tag', required=True)
    parser.add_argument('--db-output', required=True)
    parser.add_argument('--redirects', required=True)
    parser.add_argument('--gpg-key', help='GPG key ID for signing the database', default=None)
    args = parser.parse_args()

    # Read lock.json from same directory as mapping
    lock_path = Path(args.mapping).parent / 'lock.json'
    if not lock_path.exists():
        print(f"Error: lock.json not found at {lock_path}", file=sys.stderr)
        sys.exit(1)

    with open(lock_path) as f:
        lock = json.load(f)
    pkg_names = [pkg['name'] for pkg in lock['packages']]

    # Read existing mapping
    with open(args.mapping) as f:
        mapping = json.load(f)

    # Clean up: remove any package entries not in lock.json
    current_packages = mapping.get('packages', {})
    valid_keys = set(pkg_names)
    for key in list(current_packages.keys()):
        if key not in valid_keys:
            del current_packages[key]

    # Locate new package files
    new_pkgs_dir = Path(args.new_packages)
    new_pkg_files = list(new_pkgs_dir.glob('*.pkg.tar.zst'))
    if not new_pkg_files:
        print(f"Error: No .pkg.tar.zst files found in {new_pkgs_dir}", file=sys.stderr)
        sys.exit(1)

    # Update mapping
    for pkg_file in new_pkg_files:
        fname = pkg_file.name
        matched = None
        for name in pkg_names:
            if fname.startswith(name + '-'):
                matched = name
                break
        if matched is None:
            matched = fname.split('-')[0]
            print(f"Warning: Could not match {fname}, using {matched}", file=sys.stderr)

        mapping['packages'][matched] = {
            "filename": fname,
            "release_tag": args.release_tag
        }

    # Build repository database with optional signing
    db_path = Path(args.db_output)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    temp_dir = Path('/tmp/repo_build')
    temp_dir.mkdir(exist_ok=True)

    # Copy old database if exists
    if db_path.exists():
        shutil.copy(db_path, temp_dir / 'auto-aur.db.tar.gz')

    # Copy new packages to temp dir
    for pkg_file in new_pkg_files:
        shutil.copy(pkg_file, temp_dir)

    # Run repo-add
    db_file = temp_dir / 'auto-aur.db.tar.gz'
    pkg_files = list(temp_dir.glob('*.pkg.tar.zst'))
    if not pkg_files:
        print("Error: No package files found in temp dir", file=sys.stderr)
        sys.exit(1)

    cmd = ['repo-add']
    if args.gpg_key:
        cmd += ['--sign', '--key', args.gpg_key]
    cmd += [db_file] + pkg_files
    subprocess.run(cmd, check=True)

    # Copy the resulting database (and its signature) to output path
    shutil.copy(db_file, db_path)
    sig_file = db_file.with_suffix(db_file.suffix + '.sig')
    if sig_file.exists():
        shutil.copy(sig_file, db_path.with_suffix(db_path.suffix + '.sig'))

    files_tar_gz = db_file.with_suffix('').with_suffix('.files.tar.gz')
    if files_tar_gz.exists() and args.gpg_key:
        subprocess.run([
            'gpg', '--batch', '--detach-sign', '--local-user', args.gpg_key,
            str(files_tar_gz)
        ], check=True)
        # 署名ファイルもコピー先に含める
        shutil.copy(files_tar_gz.with_suffix(files_tar_gz.suffix + '.sig'),
                    db_path.with_suffix('').with_suffix('.files.tar.gz.sig'))

    # Generate _redirects file
    repo = os.environ.get('GITHUB_REPOSITORY', 'unknown/repo')
    redirect_lines = []
    for _pkgname, info in mapping['packages'].items():
        filename = info['filename']
        tag = info['release_tag']
        src = f"/repo/auto-aur/x86_64/{filename}"
        target = f"https://github.com/{repo}/releases/download/{tag}/{filename}"
        redirect_lines.append(f"{src} {target} 302")
        src = f"/repo/auto-aur/x86_64/{filename}.sig"
        target = f"https://github.com/{repo}/releases/download/{tag}/{filename}.sig"
        redirect_lines.append(f"{src} {target} 302")
    with open(args.redirects, 'w') as f:
        f.write("\n".join(redirect_lines))

    # Write updated mapping.json
    with open(args.mapping, 'w') as f:
        json.dump(mapping, f, indent=2)

if __name__ == '__main__':
    main()
