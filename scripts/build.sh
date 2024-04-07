pacman -Syu --noconfirm --needed base-devel git sudo

mkdir work
cd work
curl -O https://aur.archlinux.org/cgit/aur.git/snapshot/paru.tar.gz
tar xf paru.tar.gz
cd paru
sudo -u nobody makepkg -sci

repo-add /repo/repo.db.tar.gz paru.pkg.tar.zstd
