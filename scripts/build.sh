#!/bin/sh -ex

#yes "" | sudo -u builder paru --noconfirm
# error: no operation specified (use -h for help)
# https://distro.tube/man-org/man8/paru.8.html
# paru is paru -Syu
yes "" | sudo -u builder paru

if [ -e packages.txt ]; then
  yes "" | xargs -a packages.txt sudo -u builder paru --noconfirm --nocheck --nocleanafter -S
  rm packages.txt
fi
