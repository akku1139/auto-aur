pacman -Syu --needed base-devel git

mkdir work
cd work
curl -O https://aur.archlinux.org/cgit/aur.git/snapshot/paru.tar.gz
tar xf paru.tar.gz
cd paru
makepkg -sci

repo-add /repo/repo.db.tar.gz paru.pkg.tar.zstd
