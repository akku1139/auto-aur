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

mkdir -p repo/auto-aur/x86_64/
cd repo
# touch auto-aur.db.tar.gz
# ln -s auto-aur.db.tar.gz auto-aur.db
chown -R nobody:nobody .
cd ..

cat >> /etc/pacman.conf << EOL
[chaotic-aur]
Include = /etc/pacman.d/chaotic-mirrorlist

[auto-aur]
SigLevel = PackageOptional DatabaseOptional
Server = file://$PWD/repo/auto-aur/x86_64/
EOL

pac -Syu base-devel sudo paru

cat >> /etc/sudoers << EOL
nobody ALL=(ALL:ALL) NOPASSWD: ALL
EOL

cat >> /etc/paru.conf << EOL
[options]
LocalRepo = auto-aur
CloneDir = /tmp/buildpkg
Devel
Sign
SignDb
[bin]
PreBuildCommand = $PWD/scripts/prebuild.sh
EOL

# optimization level 3
# use pipe (faster build steps)
# disable warning
CFLAGS="-O3 -pipe -w"

cat >> /etc/makepkg.conf << EOL
PACKAGER="akku <akkun11.open (at) gmail.com>"
GPGKEY="2ECF4E27AAACF8F478631D73AA4D941DB6C633AF"

CFLAGS="$CFLAGS"
CXXFLAGS="$CFLAGS"
LDFLAGS="-flto"

MAKEFLAGS="-j6"
EOL

mkdir --mode=777 -p /.local

mkdir --mode=700 /.gnupg
cp /root/.gnupg/* /.gnupg
chown -R nobody:nobody /.gnupg
