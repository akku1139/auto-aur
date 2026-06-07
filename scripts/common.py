import urllib.request
import re
import subprocess
from pathlib import Path
from typing import Set

LOCAL_PACKAGES_DIR = Path("local-packages")
CUSTOM_PATCHES_DIR = Path("custom-patches")

def is_local_package(pkg: str) -> bool:
    return (LOCAL_PACKAGES_DIR / pkg / "PKGBUILD").exists()

def is_custom_patch(pkg: str) -> bool:
    return (CUSTOM_PATCHES_DIR / pkg / "PKGBUILD").exists()

def get_local_srcinfo(pkg: str) -> str:
    pkg_dir = LOCAL_PACKAGES_DIR / pkg
    srcinfo_file = pkg_dir / ".SRCINFO"
    return srcinfo_file.read_text()

def get_custom_srcinfo(pkg: str) -> str:
    pkg_dir = CUSTOM_PATCHES_DIR / pkg
    srcinfo_file = pkg_dir / ".SRCINFO"
    return srcinfo_file.read_text()

def get_aur_srcinfo(pkg: str) -> str:
    url = f"https://aur.archlinux.org/cgit/aur.git/plain/.SRCINFO?h={pkg}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode('utf-8')

def parse_deps(srcinfo: str) -> Set[str]:
    deps = set()
    for line in srcinfo.splitlines():
        line = line.strip()
        if line.startswith(('depends =', 'makedepends =')):
            dep = line.split('=', 1)[1].strip()
            dep = re.split(r'[>=<]+', dep)[0].strip()
            deps.add(dep)
    return deps

def is_in_repositories(pkg: str) -> bool:
    """パッケージが (公式または追加リポジトリを含む)いずれかのリポジトリに存在するか (仮想プロバイダも含む)"""
    try:
        result = subprocess.run(
            ['pacman', '-Ssq', f'^{pkg}$'],
            capture_output=True, text=True, check=False
        )
        # 出力があれば存在する (空文字列でない)
        return result.returncode == 0 and bool(result.stdout.strip())
    except:
        return False

def get_deps(pkg: str) -> Set[str]:
    if is_local_package(pkg):
        srcinfo = get_local_srcinfo(pkg)
    elif is_custom_patch(pkg):
        srcinfo = get_custom_srcinfo(pkg)
    else:
        srcinfo = get_aur_srcinfo(pkg)
    deps = parse_deps(srcinfo)
    return {d for d in deps if not is_in_repositories(d)}

def get_current_version(pkg: str) -> str:
    if is_local_package(pkg) or is_custom_patch(pkg):
        # ローカルパッケージのバージョンを PKGBUILD から読み取る
        pkgbuild_path = (LOCAL_PACKAGES_DIR / pkg / "PKGBUILD" if is_local_package(pkg)
                         else CUSTOM_PATCHES_DIR / pkg / "PKGBUILD")
        text = pkgbuild_path.read_text()
        if (match := re.search(r'^pkgver=(.+)$', text, re.M)):
            pkgver = match.group(1)
        else:
            raise ValueError("Couldn't find pkgver")
        if (match := re.search(r'^pkgrel=(.+)$', text, re.M)):
            pkgrel = match.group(1)
        else:
            raise ValueError("Couldn't find pkgver")
        return f"{pkgver}-{pkgrel}"
    else:
        srcinfo = get_aur_srcinfo(pkg)
        pkgver = pkgrel = None
        for line in srcinfo.splitlines():
            line = line.strip()
            if line.startswith('pkgver ='):
                pkgver = line.split('=',1)[1].strip()
            elif line.startswith('pkgrel ='):
                pkgrel = line.split('=',1)[1].strip()
        return f"{pkgver}-{pkgrel}" if pkgver and pkgrel else "unknown"
