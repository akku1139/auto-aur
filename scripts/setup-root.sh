# Show commands
set -x
# Error
set -e

cd $GITHUB_ACTION_PATH

# Alias
shopt -s expand_aliases
alias pac="pacman --noconfirm"

# Init pacman
pacman-key --init

# Setup Chaotic AUR
pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com
pacman-key --lsign-key 3056513887B78AEB
pac -U "https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst" \
       "https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst"

pacman-key --recv-key b465fd29d2ea44cc --keyserver keyserver.ubuntu.com
pacman-key --lsign-key b465fd29d2ea44cc

cat >> /etc/pacman.conf << EOL
[chaotic-aur]
Include = /etc/pacman.d/chaotic-mirrorlist

[auto-aur]
SigLevel = PackageOptional DatabaseOptional
Server = file://$PWD/public/repo/auto-aur/x86_64/
EOL

cat >> /etc/sudoers << EOL
root ALL=(ALL:ALL) NOPASSWD: ALL
builder ALL=(ALL:ALL) NOPASSWD: ALL
EOL

pac -Syu base-devel sudo paru python-gitpython

useradd -m builder

# Enable scripts run permission
chmod +x scripts/*

#mkdir -p public/repo/auto-aur/x86_64/
#cd public/repo/auto-aur/x86_64/
#touch auto-aur.db.tar.gz
#ln -s auto-aur.db.tar.gz auto-aur.db
#cd ../../../../
chown -R builder:builder public local
#ls -la $PWD/public/repo/auto-aur/x86_64/

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

sudo -E -u builder bash ./scripts/setup-builder.sh
