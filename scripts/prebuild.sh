#!/bin/sh

PKGNAME=`basename $PWD`

PATCHDIR=$PWD/patches/$PKGNAME/

if [ ! -e $PATCHDIR ]; then
  exit
fi

for patch in `find $PATCHDIR -maxdepth 1 -type f | sort`; do
  echo "Applying the patch:" $patch
  patch -p1 < $patch
fi
