import urllib.request
import json
import re
import subprocess
from pathlib import Path
from typing import Set, Tuple, Dict, List, Optional

LOCAL_PACKAGES_DIR = Path("local-packages")
CUSTOM_PATCHES_DIR = Path("custom-patches")

# キャッシュ: パッケージ名 -> (version, deps, pkgbase)
_aur_info_cache: Dict[str, Tuple[str, Set[str], str]] = {}
# キャッシュ: パッケージ名 -> deps（is_in_repositories 適用後）
_deps_cache: Dict[str, Set[str]] = {}
# リポジトリに存在する全パッケージ名（1回だけ取得）
_repo_pkgs_cache: Optional[Set[str]] = None


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

def _parse_dep_names(dep_list) -> Set[str]:
    deps = set()
    for dep in dep_list or []:
        dep_name = re.split(r'[>=<]+', dep)[0].strip()
        deps.add(dep_name)
    return deps

def fetch_aur_infos(pkgs: List[str]) -> Dict[str, Tuple[str, Set[str], str]]:
    """Fetch multiple AUR packages info in one request and update cache."""
    if not pkgs:
        return {}
    base_url = "https://aur.archlinux.org/rpc?v=5&type=info"
    for pkg in pkgs:
        base_url += f"&arg[]={pkg}"
    req = urllib.request.Request(base_url, headers={"User-Agent": "curl/7.68.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    if data.get("resultcount", 0) == 0:
        return {}
    result_map = {}
    for result in data["results"]:
        name = result["Name"]
        version = result.get("Version", "unknown")
        pkgbase = result.get("PackageBase", name)
        deps = _parse_dep_names(result.get("Depends")) | _parse_dep_names(result.get("MakeDepends"))
        result_map[name] = (version, deps, pkgbase)
        _aur_info_cache[name] = (version, deps, pkgbase)
    return result_map

def preload_aur_cache(pkgs: List[str]) -> None:
    """Preload multiple AUR package infos into cache using a single API call."""
    missing = [p for p in pkgs if p not in _aur_info_cache]
    if missing:
        fetch_aur_infos(missing)

def get_aur_info(pkg: str) -> Tuple[str, Set[str], str]:
    """Returns (version, deps, pkgbase) for an AUR package. Uses cache if available."""
    if pkg in _aur_info_cache:
        return _aur_info_cache[pkg]

    url = f"https://aur.archlinux.org/rpc?v=5&type=info&arg[]={pkg}"
    req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    if data.get("resultcount", 0) == 0:
        raise ValueError(f"Package {pkg} not found in AUR")
    result = data["results"][0]
    version = result.get("Version", "unknown")
    pkgbase = result.get("PackageBase", pkg)
    deps = _parse_dep_names(result.get("Depends")) | _parse_dep_names(result.get("MakeDepends"))
    _aur_info_cache[pkg] = (version, deps, pkgbase)
    return version, deps, pkgbase

def get_aur_version(pkg: str) -> str:
    version, _, _ = get_aur_info(pkg)
    return version

def get_aur_deps(pkg: str) -> Set[str]:
    _, deps, _ = get_aur_info(pkg)
    return deps

def get_aur_pkgbase(pkg: str) -> str:
    _, _, pkgbase = get_aur_info(pkg)
    return pkgbase

def parse_deps(srcinfo: str) -> Set[str]:
    deps = set()
    for line in srcinfo.splitlines():
        line = line.strip()
        if line.startswith(('depends =', 'makedepends =')):
            dep = line.split('=', 1)[1].strip()
            dep = re.split(r'[>=<]+', dep)[0].strip()
            deps.add(dep)
    return deps

def _get_all_repo_packages() -> Set[str]:
    """全リポジトリパッケージ名を1回だけ取得してキャッシュする"""
    global _repo_pkgs_cache
    if _repo_pkgs_cache is None:
        try:
            result = subprocess.run(
                ['pacman', '-Slq'],
                capture_output=True, text=True, check=False
            )
            _repo_pkgs_cache = set(result.stdout.split()) if result.returncode == 0 else set()
        except Exception:
            _repo_pkgs_cache = set()
    return _repo_pkgs_cache

def is_in_repositories(pkg: str) -> bool:
    return pkg in _get_all_repo_packages()

def get_deps(pkg: str) -> Set[str]:
    if pkg in _deps_cache:
        return _deps_cache[pkg]

    if is_local_package(pkg):
        srcinfo = get_local_srcinfo(pkg)
        deps = parse_deps(srcinfo)
    elif is_custom_patch(pkg):
        srcinfo = get_custom_srcinfo(pkg)
        deps = parse_deps(srcinfo)
    else:
        deps = get_aur_deps(pkg)

    result = {d for d in deps if not is_in_repositories(d)}
    _deps_cache[pkg] = result
    return result

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
        return get_aur_version(pkg)
