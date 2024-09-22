#!/bin/sh -e
# Stop with error
set -e
set -x

export GPG_TTY=$(tty)

paru

if [ -e packages.txt ]; then
  xargs -a packages.txt sudo -u nobody paru --noconfirm --nocheck --nocleanafter -S
  rm packages.txt
fi
