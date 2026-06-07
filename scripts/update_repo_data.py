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
    parser.add_argument('--mapping', required=True, help='Path to mapping.json (in repo-data)')
    parser.add_argument('--new-packages', required=True, help='Directory with new .pkg.tar.zst files')
    parser.add_argument('--release-tag', required=True, help='GitHub release tag for these packages')
    parser.add_argument('--db-output', required=True, help='Path where myrepo.db.tar.gz should be written')
    parser.add_argument('--redirects', required=True, help='Path to _redirects file')
    args = parser.parse_args()

    # Read lock.json from same directory as mapping (repo-data)
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

    # Locate new package files
    new_pkgs_dir = Path(args.new_packages)
    new_pkg_files = list(new_pkgs_dir.glob('*.pkg.tar.zst'))
    if not new_pkg_files:
        print(f"Error: No .pkg.tar.zst files found in {new_pkgs_dir}", file=sys.stderr)
        sys.exit(1)

    # Update mapping: match each file to a package name from lock.json
    for pkg_file in new_pkg_files:
        fname = pkg_file.name
        matched = None
        for name in pkg_names:
            if fname.startswith(name + '-'):
                matched = name
                break
        if matched is None:
            # Fallback: use first component before first dash
            matched = fname.split('-')[0]
            print(f"Warning: Could not match {fname}, using {matched}", file=sys.stderr)

        mapping['packages'][matched] = {
            "filename": fname,
            "release_tag": args.release_tag
        }

    # Build the repository database (repo-add)
    db_path = Path(args.db_output)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    temp_dir = Path('/tmp/repo_build')
    temp_dir.mkdir(exist_ok=True)

    # Copy old database if it exists
    if db_path.exists():
        shutil.copy(db_path, temp_dir / 'myrepo.db.tar.gz')

    # Copy new packages to temp dir
    for pkg_file in new_pkg_files:
        shutil.copy(pkg_file, temp_dir)

    # Run repo-add
    db_file = temp_dir / 'myrepo.db.tar.gz'
    pkg_files = list(temp_dir.glob('*.pkg.tar.zst'))
    if not pkg_files:
        print("Error: No package files found in temp dir", file=sys.stderr)
        sys.exit(1)

    cmd = ['repo-add', db_file] + pkg_files
    subprocess.run(cmd, check=True)

    # Copy the resulting database to output path
    shutil.copy(db_file, db_path)

    # Generate _redirects file
    repo = os.environ.get('GITHUB_REPOSITORY', 'unknown/repo')
    redirect_lines = []
    for pkgname, info in mapping['packages'].items():
        filename = info['filename']
        tag = info['release_tag']
        src = f"/pool/{filename}"
        target = f"https://github.com/{repo}/releases/download/{tag}/{filename}"
        redirect_lines.append(f"{src} {target} 302")
    with open(args.redirects, 'w') as f:
        f.write("\n".join(redirect_lines))

    # Write updated mapping.json
    with open(args.mapping, 'w') as f:
        json.dump(mapping, f, indent=2)

if __name__ == '__main__':
    main()
