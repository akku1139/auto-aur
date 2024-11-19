#!/bin/sh -ex
basepath=$( pwd )

#yes "" | sudo -u builder paru --noconfirm
# error: no operation specified (use -h for help)
# https://distro.tube/man-org/man8/paru.8.html
# paru is paru -Syu
paru

# xargs -a packages.txt sudo -u builder paru --noconfirm --nocheck --nocleanafter -S
for pkg in $( cat packages.txt non-aur/non-aur.txt); do
  if [ "$pkg" = "" ]; then
    continue
  fi

  case $( echo "$pkg" | cut -d ":" -f1 ) in
    git)
      repo=$( echo "$pkg" | cut -c 5- )
      confdir="non-aur/git-$( echo "$repo" | base64 )"
      new="n"

      lc=$( git ls-remote -qh "$repo" | cut -f1 )

      if [ ! -d "$confdir" ]; then
        mkdir "$confdir"
        echo "$lc" > "$confdir/latest-commit"
        new="y"
      fi

      if [ "$lc" != $( echo "$confdir/latest-commit" ) ]; then
        echo "$lc" > $confdir/latest-commit
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

  if [ "$new" = "y" ]; then
    echo "$pkg" >> non-aur/non-aur.txt
  fi
done

echo > packages.txt
