#!/bin/sh -ex

paru

if [ -e packages.txt ]; then
  xargs -a packages.txt sudo -u nobody paru --noconfirm --nocheck --nocleanafter -S
  rm packages.txt
fi
