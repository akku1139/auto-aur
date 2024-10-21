#!/bin/sh -ex

sudo -u builder paru

if [ -e packages.txt ]; then
  xargs -a packages.txt sudo -u builder paru --noconfirm --nocheck --nocleanafter -S
  rm packages.txt
fi
