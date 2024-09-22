#!/bin/sh -e
# Stop with error
set -e
set -x

faketty paru

if [ -e packages.txt ]; then
  xargs -a packages.txt sudo -u nobody faketty paru --noconfirm --nocheck --nocleanafter -S
  rm packages.txt
fi
