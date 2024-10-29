#!/bin/sh -ex

#yes "" | sudo -u builder paru --noconfirm
# error: no operation specified (use -h for help)
yes "" | sudo -u builder paru

if [ -e packages.txt ]; then
  yes "" | xargs -a packages.txt sudo -u builder paru --noconfirm --nocheck --nocleanafter -S
  rm packages.txt
fi
