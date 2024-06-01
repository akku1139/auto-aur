# Show commands
set -x

pacman -Sy --noconfirm
pacman-key --init

# Setup Chaotic AUR
pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com
pacman-key --lsign-key 3056513887B78AEB
pacman -U "https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst"
pacman -U "https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst"
cat > /etc/pacman.conf << EOL
[chaotic-aur]
Include = /etc/pacman.d/chaotic-mirrorlist
EOL

# Setup CachyOS
pacman-key --recv-keys F3B607488DB35A47 --keyserver keyserver.ubuntu.com
pacman-key --lsign-key F3B607488DB35A47
pacman -U "https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-keyring-20240331-1-any.pkg.tar.zst" \
          "https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-mirrorlist-18-1-any.pkg.tar.zst"
cat > /etc/pacman.conf << EOL
[cachyos]
Include = /etc/pacman.d/cachyos-mirrorlist
EOL

pacman -Syu --noconfirm --needed base-devel git sudo paru

repo-add /repo/repo.db.tar.gz paru.pkg.tar.zstd
