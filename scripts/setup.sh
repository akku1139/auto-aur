# Show commands
set -x

# Alias
shopt -s expand_aliases
alias pac="pacman --noconfirm"
alias pr="sudo -u nobody paru --noconfirm"

# Enable scripts run permission
chmod +x scripts/*

# Init pacman
# pac -Syyu
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

[aur]
SigLevel = PackageOptional DatabaseOptional
Server = file://$PWD/repo
EOL

pac -Syu base-devel sudo paru

cat >> /etc/sudoers << EOL
nobody ALL=(ALL:ALL) NOPASSWD: ALL
EOL

cat >> /etc/paru.conf << EOL
[options]
LocalRepo = aur
[bin]
PreBuildCommand = $PWD/scripts/prebuild.sh
EOL

mkdir -p /home/nobody
usermod -d /home/nobody nobody
chmod -R 777 $PWD/repo
