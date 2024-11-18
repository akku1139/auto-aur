#!/bin/sh -ex
basepath=$( pwd )

#yes "" | sudo -u builder paru --noconfirm
# error: no operation specified (use -h for help)
# https://distro.tube/man-org/man8/paru.8.html
# paru is paru -Syu
sudo -u builder paru

if [ -e packages.txt ]; then
  # xargs -a packages.txt sudo -u builder paru --noconfirm --nocheck --nocleanafter -S
  for pkg in $(cat packages.txt); do
    case `echo $p | cut -c -4` in
      git:)
        repo=$( echo $pkg | cut -c 5- )
        confdir=$(cd "non-aur/git-$( echo $repo | base64 )" && pwd)

        lc=$( git ls-remote -qh $repo | cut -f1 )

        if [! -d  $confdir ]; then
          mkdir $confdir
          echo $lc > $confdir/latest-commit
        fi

        if [ $lc != $( echo $confdir/latest-commit ) ]; then
          echo $lc > $confdir/latest-commit
          workdir=$( cd $( mktemp --directory --tmpdir=work ) && pwd )
          cd $workdir
          git clone --depth=1 $repo .
          sudo -u builder paru -U
        fi
        ;;
      *)
        sudo -u builder paru --noconfirm --nocheck --nocleanafter -S $pkg
        ;;
    esac
    cd $basepath
  done
  rm packages.txt
fi
