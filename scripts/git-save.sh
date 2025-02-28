#!/bin/bash
set -ex
#cd "$( dirname $0 )/../"
cd /__w/auto-aur/auto-aur

if [ -n "$(git status --porcelain)" ]; then
  git pull
  python scripts/genui.py
  git add -A
  git commit -m "Data"
  git push
fi
