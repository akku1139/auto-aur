#!/bin/sh

#set -ex
set -e

P=$PWD
cd "$( dirname $0 )/../"
# if [ -n "$(git status --porcelain)" ]; then
  git pull
  python scripts/genui.py
  git add -A
  git commit -m "Data"
  git push
# fi
cd "$P"

PKGNAME=`basename $PWD`
PATCHDIR="$( dirname $0 )/../patches/$PKGNAME"

echo ":: Running prebuild commands for $PKGNAME"

if [ ! -d $PATCHDIR ]; then
  exit
fi

if [ -f $PATCHDIR/deps ]; then
  echo ":: Installing additional deps..."
  sudo pacman --noconfirm -S $( cat $PATCHDIR/deps )
fi

echo ":: Patching $PKGNAME..."

if [ ! -f $PATCHDIR/version ]; then
  echo "Warn (prebuild.sh): $PATCHDIR/version was not found"
else
  targetver=$( awk '$1=="pkgver" {v=$3} $1=="pkgrel" {r=$3} $1=="epoch" {e=$3":"} END {print e v "-" r}' .SRCINFO )
  patchver=$( cat "$PATCHDIR/version" )
  if  [ $targetver != $patchver ]; then
    echo "Warn (prebuild.sh): patch version and package version are different. Ignored."
    echo "Package: $PKGNAME "
    echo "Target version: $targetver"
    echo "Patch: $patchver"
    exit
  fi
fi

for patch in $( find $PATCHDIR/pre/ -maxdepth 1 -type f | sort ); do
  echo "Applying a patch:" $patch
  patch -p1 < $patch
done

if [ -d $PATCHDIR/source/ ]; then
  cp $PATCHDIR/source/* ./
fi
