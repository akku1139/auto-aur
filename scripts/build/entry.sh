#!/bin/bash

set -ex
pacman -Sy
chown -R builder:builder /home/builder/pkg
cd /home/builder/pkg
if [ -s deps ]; then
  pacman -S --asdeps --noconfirm $(cat deps)
fi
cd src
sudo -u builder makepkg -s --noconfirm --skippgpcheck
cp *.pkg.tar.zst /repo/

for f in *.pkg.tar.zst; do
  pkgname=$(bsdtar -xO -f "$f" .PKGINFO | awk -F' = ' '/^pkgname /{print $2; exit}')
  echo "${f} ${pkgname}" >> /repo/pkgname-map.txt
done
