#!/bin/sh -e
# Stop with error
set -e
set -x

faketty paru

if [ -e packages.txt ]; then
  faketty xargs -a packages.txt sudo -u nobody paru --noconfirm --nocheck --nocleanafter -S
  rm packages.txt
fi
