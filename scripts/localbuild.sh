#!/bin/sh

for pkg in `ls -d local/*/`; do
  cd $pkg
  sudo -u builder paru -U
  cd ../..
done
