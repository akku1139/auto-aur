#!/bin/sh

#set -ex
set -e

echo ":: Running prebuild commands"

PKGNAME=`basename $PWD`
PATCHDIR="$( dirname $0 )/../patches/$PKGNAME"

if [ ! -d $PATCHDIR ]; then
  exit
fi

if [ -f $PATCHDIR/deps ]; then
  sudo pacman --noconfirm -S $( cat $PATCHDIR/deps )
fi

targetver=$( awk '$1=="pkgver" {v=$3} $1=="pkgrel" {r=$3} $1=="epoch" {e=$3":"} END {print e v "-" r}' .SRCINFO )
patchver=$( cat "$PATCHDIR/version" )
if [ $targetver != $patchver ]; then
  echo "Error (prebuild.sh): Patch version and package version are different"
  echo "Package: $targetver"
  echo "Patch: $patchver"
  echo "Exit."
  exit 1
fi

for patch in $( find $PATCHDIR/pre/ -maxdepth 1 -type f | sort ); do
  echo "Applying a patch:" $patch
  patch -p1 < $patch
done

if [ -d $PATCHDIR/source/ ]; then
  cp $PATCHDIR/source/* ./
fi
