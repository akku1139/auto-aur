# Show commands
set -x

# Alias
shopt -s expand_aliases
alias pac="pacman --noconfirm"

# Enable scripts run permission
chmod +x scripts/*

# Init pacman
pacman-key --init

# Setup Chaotic AUR
pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com
pacman-key --lsign-key 3056513887B78AEB
pac -U "https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst" \
       "https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst"

# Setup CachyOS
#pacman-key --recv-keys F3B607488DB35A47 --keyserver keyserver.ubuntu.com
#pacman-key --lsign-key F3B607488DB35A47
#pac -U "https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-keyring-20240331-1-any.pkg.tar.zst" \
#       "https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-mirrorlist-18-1-any.pkg.tar.zst"
#cat > /etc/pacman.conf << EOL
#[cachyos]
#Include = /etc/pacman.d/cachyos-mirrorlist
#EOL

cat >> /etc/pacman.conf << EOL
[chaotic-aur]
Include = /etc/pacman.d/chaotic-mirrorlist
EOL

pac -Syu base-devel sudo paru

cat >> /etc/sudoers << EOL
nobody ALL=(ALL:ALL) NOPASSWD: ALL
EOL

cat >> /etc/pacman.conf << EOL
[auto-aur]
SigLevel = PackageOptional DatabaseOptional
# Server = file://${PWD}/repo
Server = file:///tmp/repo
EOL

cat >> /etc/paru.conf << EOL
[options]
LocalRepo = auto-aur
CloneDir = /tmp/buildpkg
[bin]
PreBuildCommand = $PWD/scripts/prebuild.sh
EOL

mkdir --mode=777 -p /.local

paru
