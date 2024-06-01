#!/bin/sh

for pkg in `find $PWD/local -type d -maxdepth 1`; do
  cd pkg
  paru -U
done
