import urllib.request
import urllib.parse
import json
import re
import subprocess
from pathlib import Path
from typing import Set, Tuple, Dict, List, Optional
import glob
import os
import pyalpm

LOCAL_PACKAGES_DIR = Path("local-packages")
CUSTOM_PATCHES_DIR = Path("custom-patches")

# キャッシュ: パッケージ名 -> (version, deps, pkgbase)
_aur_info_cache: Dict[str, Tuple[str, Set[str], str]] = {}
# キャッシュ: パッケージ名 -> deps（is_in_repositories 適用後）
_deps_cache: Dict[str, Set[str]] = {}
# pkg名 -> リポジトリ(provides込み)で満たされるか
_repo_provides_cache: Optional[Set[str]] = None


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

def preload_aur_cache(pkgs: list[str]) -> None:
    """Preload multiple AUR package infos into cache using batched API calls."""
    missing = [p for p in pkgs if p not in _aur_info_cache]
    # 200件ずつに分割して取得（AUR RPCのURL長対策）
    for i in range(0, len(missing), 200):
        chunk = missing[i:i+200]
        fetch_aur_infos(chunk)

def get_aur_info(pkg: str) -> Tuple[str, Set[str], str]:
    """Returns (version, deps, pkgbase) for an AUR package. Uses cache if available."""
    if pkg in _aur_info_cache:
        return _aur_info_cache[pkg]

    url = f"https://aur.archlinux.org/rpc?v=5&type=info&arg[]={urllib.parse.quote(pkg)}"
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


def parse_vcs_source(srcinfo: str) -> Optional[Tuple[str, str]]:
    """Extract (url, fragment) from the first git VCS source in .SRCINFO."""
    for line in srcinfo.splitlines():
        line = line.strip()
        if line.startswith('source = '):
            src = line.split(' = ', 1)[1].strip()
            url = None
            frag = ''
            if src.startswith('git+'):
                rest = src[4:]
                if '#' in rest:
                    url, frag = rest.split('#', 1)
                else:
                    url = rest
            elif src.startswith('git://'):
                if '#' in src:
                    url, frag = src.split('#', 1)
                else:
                    url = src
            if url:
                return url, frag
    return None


def _git_ls_remote(url: str, ref: Optional[str]) -> Optional[str]:
    cmd = ['git', 'ls-remote', url]
    if ref:
        cmd.append(ref)
    else:
        cmd.append('HEAD')
    try:
        out = subprocess.check_output(
            cmd,
            text=True,
            timeout=20,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return None
    if not out:
        return None
    first_line = out.splitlines()[0]
    return first_line.split('\t')[0]


_vcs_ref_cache: Dict[str, Optional[str]] = {}


def get_vcs_ref(url: str, ref: Optional[str]) -> Optional[str]:
    cache_key = f"{url}#{ref}"
    if cache_key in _vcs_ref_cache:
        return _vcs_ref_cache[cache_key]
    result = _git_ls_remote(url, ref)
    _vcs_ref_cache[cache_key] = result
    return result


def fetch_aur_srcinfo(pkgbase: str) -> str:
    """Fetch .SRCINFO for an AUR package base from cgit."""
    url = (
        "https://aur.archlinux.org/cgit/aur.git/plain/.SRCINFO?h="
        + urllib.parse.quote(pkgbase)
    )
    req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
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

def _get_repo_provides_map() -> Set[str]:
    global _repo_provides_cache
    if _repo_provides_cache is not None:
        return _repo_provides_cache

    handle = pyalpm.Handle("/", "/var/lib/pacman")
    names: Set[str] = set()

    sync_dir = "/var/lib/pacman/sync"
    for db_file in sorted(glob.glob(os.path.join(sync_dir, "*.db"))):
        repo_name = os.path.basename(db_file)[:-3]  # ".db" を除去
        try:
            db = handle.register_syncdb(repo_name, pyalpm.SIG_DATABASE_OPTIONAL)
        except pyalpm.error:
            continue
        for pkg in db.pkgcache:
            names.add(pkg.name)
            for prov in pkg.provides:
                prov_name = re.split(r'[>=<]+', prov)[0].strip()
                names.add(prov_name)

    _repo_provides_cache = names
    return names

def is_in_repositories(pkg: str) -> bool:
    return pkg in _get_repo_provides_map()

def get_deps(pkg: str) -> Set[str]:
    if pkg in _deps_cache:
        return _deps_cache[pkg]

    if is_local_package(pkg):
        deps = parse_deps(get_local_srcinfo(pkg))
    elif is_custom_patch(pkg):
        deps = parse_deps(get_custom_srcinfo(pkg))
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
