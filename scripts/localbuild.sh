#!/bin/sh

for pkg in `ls -d local/*/`; do
  cd $pkg
  paru -U
  cd ../..
done
