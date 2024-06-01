# Show commands
set -x

# Alias
shopt -s expand_aliases
alias pac="pacman --noconfirm"

# Init pacman
awk -i inplace '{print; if ($0 == "[options]") {print "Architecture = auto";}}' /etc/pacman.conf
pac -Syyu
pacman-key --init

# Setup Chaotic AUR
pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com
pacman-key --lsign-key 3056513887B78AEB
pac -U "https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst" \
       "https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst"
cat >> /etc/pacman.conf << EOL
[chaotic-aur]
Include = /etc/pacman.d/chaotic-mirrorlist
EOL

# Setup CachyOS
#pacman-key --recv-keys F3B607488DB35A47 --keyserver keyserver.ubuntu.com
#pacman-key --lsign-key F3B607488DB35A47
#pac -U "https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-keyring-20240331-1-any.pkg.tar.zst" \
#       "https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-mirrorlist-18-1-any.pkg.tar.zst"
#cat > /etc/pacman.conf << EOL
#[cachyos]
#Include = /etc/pacman.d/cachyos-mirrorlist
#EOL

cat /etc/pacman.conf

pac -Syu base-devel git sudo paru

repo-add ./repo/repo.db.tar.gz
