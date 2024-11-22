#!/bin/sh

set -ex

PKGNAME=`basename $PWD`
PATCHDIR=`dirname $0`/../patches/$PKGNAME

if [ ! -d $PATCHDIR ]; then
  exit
fi

if [ -f $PATCHDIR/deps ]; then
  sudo pacman --noconfirm -S $( cat $PATCHDIR/deps )
fi

for patch in `find $PATCHDIR/pre/ -maxdepth 1 -type f | sort`; do
  echo "Applying the patch:" $patch
  patch -p1 < $patch
done

if [ -d $PATCHDIR/source/ ]; then
  cp $PATCHDIR/source/* ./
fi
