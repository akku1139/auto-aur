#!/bin/sh -e
# Stop with error
set -e

paru

if [ -e packages.txt ]; then
  rm packages.txt
  xargs -a packages.txt sudo -u nobody paru --noconfirm -S
fi
