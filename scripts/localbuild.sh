#!/bin/sh

for pkg in `ls -d local/*/`; do
  cd $pkg
  sudo -u nobody paru -U
  cd ../..
done
