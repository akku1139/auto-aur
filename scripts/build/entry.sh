#!/bin/bash

set -ex
pacman -Sy
chown -R builder:builder /home/builder/pkg
cd /home/builder/pkg
if [ -s deps ]; then
  pacman -S --asdeps $(cat deps)
fi
cd src
sudo -u builder makepkg -s --noconfirm --skippgpcheck
cp *.pkg.tar.zst /repo/
