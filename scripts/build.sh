#!/bin/sh -ex

# yes "" | sudo -u builder paru --noconfirm
sudo -u builder paru --noconfirm

if [ -e packages.txt ]; then
  yes "" | xargs -a packages.txt sudo -u builder paru --noconfirm --nocheck --nocleanafter -S
  rm packages.txt
fi
