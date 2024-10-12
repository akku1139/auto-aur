#!/bin/sh

set -ex

PKGNAME=`basename $PWD`
PATCHDIR=`dirname $0`/../patches/$PKGNAME/

if [ ! -e $PATCHDIR ]; then
  exit
fi

makepkg --nobuild

for patch in `find $PATCHDIR/pre/ -maxdepth 1 -type f | sort`; do
  echo "Applying the patch:" $patch
  patch -p1 < $patch
done

if [ -d $PATCHDIR/prepare ]; then
  cp -r $PATCHDIR/prepare ./patches
fi
