wget --no-verbose https://geo.mirror.pkgbuild.com/iso/latest/archlinux-bootstrap-x86_64.tar.gz
tar xzf archlinux-bootstrap-x86_64.tar.gz --strip-components 1

echo 'Server = https://geo.mirror.pkgbuild.com/$repo/os/$arch' >> etc/pacman.d/mirrorlist
