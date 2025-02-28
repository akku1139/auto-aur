#!/bin/bash -p
# https://l-w-i.net/t/solaris/conf_002.txt
set -ex
cd "$( dirname $0 )/../"

pwd
whoami

if [ -n "$(git status --porcelain)" ]; then
  git pull
  python scripts/genui.py
  git add -A
  git commit -m "Data"
  git push
fi
