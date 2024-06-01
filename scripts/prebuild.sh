#!/bin/sh

echo "---------- Start prebuild.sh ----------"

PKGNAME=`basename $PWD`

PATCHDIR=$ROOTDIR/patches/$PKGNAME/
echo "PATCHDIR:" $PATCHDIR

if [ ! -e $PATCHDIR ]; then
  exit
fi

for patch in `find $PATCHDIR -maxdepth 1 -type f | sort`; do
  echo "Applying the patch:" $patch
  patch -p1 < $patch
fi

echo "---------------------------------------"
