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

  new="n"

  case $( echo "$pkg" | cut -d ":" -f1 ) in
    git) #Git: git:URL
      repo=$( echo "$pkg" | cut -c 5- )
      confdir="non-aur/git-$( echo "$repo" | base64 )"

      lc=$( git ls-remote -qh "$repo" | cut -f1 )

      if [ ! -d "$confdir" ]; then
        mkdir "$confdir"
        echo "$repo" > "$confdir/repo"
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

    git-mono) # Git monorepo (wip): git-mono:URL dir
      repo=$( echo "$pkg" | cut -c 10- | cut -d " " -f1 )
      dir=$( echo "$pkg" | cut -c 10- | cut -d " " -f2 )
      confdir="non-aur/git-mono-$( echo "$repo-$dir" | base64 )"

      lc=$( git ls-remote -qh "$repo" | cut -f1 )

      if [ ! -d "$confdir" ]; then
        mkdir "$confdir"
        echo "$repo" > "$confdir/repo"
        echo "$dir" > "$confdir/dir"
        echo "$lc" > "$confdir/latest-commit"
        new="y"
      fi

      if [ "$lc" != $( echo "$confdir/latest-commit" ) ]; then
        echo "$lc" > $confdir/latest-commit
        workdir=$( cd $( mktemp --directory --tmpdir=work ) && pwd )
        cd "$workdir"
        git clone --depth=1 --filter=blob:none --sparse "$repo" .
        git sparse-checkout add "$dir"
        cd "$dir"
        paru -U
      fi
      ;;

    local) # Local packages (local/): local:auto-aur-keyring
      repo=$( echo "$pkg" | cut -c 7- )
      confdir="non-aur/local-$( echo "$repo" | base64 )"
      workdir=$( cd $( mktemp --directory --tmpdir=work ) && pwd )

      if [ ! -d "$confdir" ]; then
        mkdir "$confdir"
        echo "$repo" > "$confdir/package"
        cd "local/$repo"
        makepkg --printsrcinfo > "$confdir/srcinfo"
        new="y"
        cd "$basepath"
      fi

      cd "local/$repo"
      makepkg --printsrcinfo > "$workdir/srcinfo"
      cd "$basepath"
      diff "$confdir/srcinfo" "$workdir/srcinfo"  > /dev/null 2>&1
      if [ $? -eq 1 ]; then
        cd "$basepath/local/$repo"
        makepkg --printsrcinfo > "$confdir/srcinfo"
        paru -U
      fi
      ;;

    *) # Normal AUR: pkg
      paru --noconfirm --nocheck --nocleanafter -S "$pkg"
      echo "$pkg" >> packages-manually.txt
      ;;
  esac

  cd "$basepath"

  if [ "$new" = "y" ]; then
    echo "$pkg" >> non-aur/non-aur.txt
  fi
done

echo > packages.txt
