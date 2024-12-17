#!/bin/sh
set -ex
cd public

for file in `find -size +25M -type f`; do
  rm $file
  echo "$file" "https://akku1139.github.io/auto-aur/$file" 302 >> _redirects
done
