#!/bin/sh -ex
basepath=$( pwd )

#yes "" | sudo -u builder paru --noconfirm
# error: no operation specified (use -h for help)
# https://distro.tube/man-org/man8/paru.8.html
# paru is paru -Syu
paru

if [ -e packages.txt ]; then
  # xargs -a packages.txt sudo -u builder paru --noconfirm --nocheck --nocleanafter -S
  for pkg in $(cat packages.txt); do
    if [ "$pkg" = "" ]; then
      continue
    fi

    case `echo "$pkg" | cut -c -4` in
      git:)
        repo=$( echo "$pkg" | cut -c 5- )
        confdir="non-aur/git-$( echo "$repo" | base64 )"

        lc=$( git ls-remote -qh "$repo" | cut -f1 )

        if [ ! -d "$confdir" ]; then
          mkdir "$confdir"
          echo "$lc" > "$confdir/latest-commit"
        fi

        if [ "$lc" != $( echo "$confdir/latest-commit" ) ]; then
          echo $lc > $confdir/latest-commit
          workdir=$( cd $( mktemp --directory --tmpdir=work ) && pwd )
          cd "$workdir"
          git clone --depth=1 "$repo" .
          paru -U
        fi
        ;;
      *)
        paru --noconfirm --nocheck --nocleanafter -S "$pkg"
        ;;
    esac
    cd "$basepath"
  done
  rm packages.txt
fi
