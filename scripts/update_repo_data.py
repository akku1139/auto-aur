#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys
import argparse
from pathlib import Path


def extract_pkgname_from_package_file(pkg_file):
    """Extract pkgname from .PKGINFO inside a package file."""
    try:
        out = subprocess.check_output(
            ["bsdtar", "-xOf", str(pkg_file), ".PKGINFO"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        for line in out.splitlines():
            if line.startswith("pkgname = "):
                return line.split(" = ", 1)[1].strip()
    except Exception:
        pass
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mapping', required=True)
    parser.add_argument('--new-packages', required=True)
    parser.add_argument('--release-tag', required=True)
    parser.add_argument('--db-output', required=True)
    parser.add_argument('--redirects', required=True)
    parser.add_argument('--gpg-key', help='GPG key ID for signing the database', default=None)
    parser.add_argument('--remove-packages', help='File containing package names to remove from repo')
    parser.add_argument('--pkgbase', help='pkgbase currently being built')
    args = parser.parse_args()

    # Read lock.json from same directory as mapping
    lock_path = Path(args.mapping).parent / 'lock.json'
    if not lock_path.exists():
        print(f"Error: lock.json not found at {lock_path}", file=sys.stderr)
        sys.exit(1)

    with open(lock_path) as f:
        lock = json.load(f)
    pkg_names = [pkg['name'] for pkg in lock['packages']]
    lock_versions = {pkg['name']: pkg.get('version', '') for pkg in lock['packages']}
    lock_vcs_refs = {pkg['name']: pkg.get('vcs_ref') for pkg in lock['packages']}

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
    pkgname_map = {}
    map_file = new_pkgs_dir / 'pkgname-map.txt'
    if map_file.exists():
        for line in map_file.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            fname, pkgname = line.split(' ', 1)
            pkgname_map[fname] = pkgname

    for pkg_file in new_pkg_files:
        fname = pkg_file.name
        matched = pkgname_map.get(fname)
        if matched is None:
            # fallback
            for name in pkg_names:
                if fname.startswith(name + '-'):
                    matched = name
                    break
        if matched is None:
            # .PKGINFO から正確な pkgname を取得する
            matched = extract_pkgname_from_package_file(pkg_file)
        if matched is None:
            matched = fname.split('-')[0]
            print(f"Warning: Could not match {fname}, using {matched}", file=sys.stderr)

        entry = {
            "filename": fname,
            "release_tag": args.release_tag,
            "version": lock_versions.get(matched, ""),
        }
        vcs_ref = lock_vcs_refs.get(matched)
        if vcs_ref:
            entry["vcs_ref"] = vcs_ref
        mapping['packages'][matched] = entry

    # ローカル/カスタムパッケージの pkgbase は実ファイルが無い場合があるため、
    # lock.json に登録されている名前とバージョンを mapping に反映する。
    if args.pkgbase:
        for pkg in lock["packages"]:
            if not (pkg.get("local") or pkg.get("custom")):
                continue
            if pkg["name"] != args.pkgbase:
                continue
            entry = mapping["packages"].get(pkg["name"])
            if entry is None or not entry.get("filename"):
                new_entry = {
                    "filename": "",
                    "release_tag": args.release_tag,
                    "version": lock_versions.get(pkg["name"], ""),
                }
                vcs_ref = lock_vcs_refs.get(pkg["name"])
                if vcs_ref:
                    new_entry["vcs_ref"] = vcs_ref
                mapping["packages"][pkg["name"]] = new_entry
            break

    # Build repository database with optional signing
    db_path = Path(args.db_output)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    temp_dir = Path('/tmp/repo_build')
    temp_dir.mkdir(exist_ok=True)

    # Remove packages that no longer exist in AUR
    remove_pkgs = []
    if args.remove_packages and Path(args.remove_packages).exists():
        remove_pkgs = [
            line.strip() for line in Path(args.remove_packages).read_text().splitlines()
            if line.strip()
        ]

    temp_dir = Path('/tmp/repo_build')
    shutil.rmtree(temp_dir, ignore_errors=True)
    temp_dir.mkdir(exist_ok=True)

    # Copy old database if exists
    if db_path.exists():
        shutil.copy(db_path, temp_dir / 'auto-aur.db.tar.gz')

    # Remove deleted packages from the old database
    if remove_pkgs:
        db_file_temp = temp_dir / 'auto-aur.db.tar.gz'
        if db_file_temp.exists():
            subprocess.run(
                ['repo-remove', db_file_temp] + remove_pkgs,
                check=False,  # パッケージが存在しない場合もあるため
            )

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

    files_tar_gz = temp_dir / 'auto-aur.files.tar.gz'
    shutil.copy(files_tar_gz, db_path.parent / 'auto-aur.files.tar.gz')
    files_sig_file = files_tar_gz.with_suffix(db_file.suffix + '.sig')
    if files_sig_file.exists():
        shutil.copy(files_sig_file, db_path.parent / 'auto-aur.files.tar.gz.sig')

    # Generate _redirects file
    repo = os.environ.get('GITHUB_REPOSITORY', 'unknown/repo')
    redirect_lines = []
    for _pkgname, info in mapping['packages'].items():
        filename = info.get('filename')
        if not filename:
            continue
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
