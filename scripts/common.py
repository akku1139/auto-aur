import urllib.request
import json
import re
import subprocess
from pathlib import Path
from typing import Set, Tuple

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

# ---- AUR RPC API を使用した情報取得 ----
def get_aur_info(pkg: str) -> Tuple[str, Set[str]]:
    """Returns (version, set_of_dependencies) for an AUR package using the RPC API."""
    url = f"https://aur.archlinux.org/rpc?v=5&type=info&arg[]={pkg}"
    req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    if data.get("resultcount", 0) == 0:
        raise ValueError(f"Package {pkg} not found in AUR")
    result = data["results"][0]
    version = result.get("Version", "unknown")
    deps = set()
    for dep in result.get("Depends", []) or []:
        # remove version constraints
        dep_name = re.split(r'[>=<]+', dep)[0].strip()
        deps.add(dep_name)
    for dep in result.get("MakeDepends", []) or []:
        dep_name = re.split(r'[>=<]+', dep)[0].strip()
        deps.add(dep_name)
    return version, deps

def get_aur_version(pkg: str) -> str:
    """Return only the version string for an AUR package."""
    version, _ = get_aur_info(pkg)
    return version

def get_aur_deps(pkg: str) -> Set[str]:
    """Return only the dependencies (as a set of package names) for an AUR package."""
    _, deps = get_aur_info(pkg)
    return deps

# ---- 既存のヘルパー関数（ローカル・カスタムパッケージ用） ----
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
    """Check if package exists in any enabled repository (including virtual providers)."""
    try:
        result = subprocess.run(
            ['pacman', '-Ssq', f'^{pkg}$'],
            capture_output=True, text=True, check=False
        )
        return result.returncode == 0 and bool(result.stdout.strip())
    except:
        return False

def get_deps(pkg: str) -> Set[str]:
    if is_local_package(pkg):
        srcinfo = get_local_srcinfo(pkg)
        deps = parse_deps(srcinfo)
    elif is_custom_patch(pkg):
        srcinfo = get_custom_srcinfo(pkg)
        deps = parse_deps(srcinfo)
    else:
        deps = get_aur_deps(pkg)
    # Keep only dependencies that are not satisfied by repositories
    return {d for d in deps if not is_in_repositories(d)}

def _parse_version_from_srcinfo_lines(lines):
    pkgver = pkgrel = None
    for line in lines:
        line = line.strip()
        if line.startswith('pkgver ='):
            pkgver = line.split('=', 1)[1].strip()
        elif line.startswith('pkgrel ='):
            pkgrel = line.split('=', 1)[1].strip()
    return f"{pkgver}-{pkgrel}" if pkgver and pkgrel else "unknown"

def get_current_version(pkg: str) -> str:
    if is_local_package(pkg):
        srcinfo_path = LOCAL_PACKAGES_DIR / pkg / ".SRCINFO"
        with open(srcinfo_path) as f:
            return _parse_version_from_srcinfo_lines(f)
    elif is_custom_patch(pkg):
        srcinfo_path = CUSTOM_PATCHES_DIR / pkg / ".SRCINFO"
        with open(srcinfo_path) as f:
            return _parse_version_from_srcinfo_lines(f)
    else:
        # AUR package - use API
        return get_aur_version(pkg)
