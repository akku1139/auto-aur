#!/bin/sh -ex
basepath=$( pwd )
PARU="paru --ask=4 --noconfirm"
#export PATH="$basepath/scripts/wrapper:$PATH"

#yes "" | sudo -u builder paru --noconfirm
# error: no operation specified (use -h for help)
# https://distro.tube/man-org/man8/paru.8.html
# paru is paru -Syu
# https://bbs.archlinux.org/viewtopic.php?id=35901 (pacman --ask)
#$PARU -Syu || true

# if [ -n "$(git status --porcelain)" ]; then
#   git pull
#   git add -A
#   git commit -m "Data"
#   git push
# fi

# xargs -a packages.txt sudo -u builder paru --noconfirm --nocheck --nocleanafter -S
cat packages.txt non-aur/non-aur.txt | { while read pkg; do
  if [ "$pkg" = "" ]; then
    continue
  fi

  new="n"
  workdir=$( cd $( mktemp --directory --tmpdir=work ) && pwd )

  echo target $pkg

  case $( echo "$pkg" | cut -d ":" -f1 ) in
    git) #Git: git:URL
      repo=$( echo "$pkg" | cut -c 5- )
      confdir="$basepath/non-aur/git-$( echo "$repo" | sha256sum | cut -d " " -f1 )"

      lc=$( git ls-remote -qh "$repo" )

      if [ ! -d "$confdir" ]; then
        mkdir "$confdir"
        echo "$repo" > "$confdir/repo"
        echo "$lc" > "$confdir/latest-commit"
        new="y"
      fi

      if [ "$lc" != $( echo "$confdir/latest-commit" ) ]; then
        cd "$workdir"
        git clone --depth=1 "$repo" .
        $PARU -U
        echo "$lc" > $confdir/latest-commit
      fi
      ;;

    git-mono) # Git monorepo (wip): git-mono:URL dir
      repo=$( echo "$pkg" | cut -c 10- | cut -d " " -f1 )
      dir=$( echo "$pkg" | cut -c 10- | cut -d " " -f2 )
      confdir="$basepath/non-aur/git-mono-$( echo "$repo-$dir" | sha256sum | cut -d " " -f1 )"

      lc=$( git ls-remote -qh "$repo" )

      if [ ! -d "$confdir" ]; then
        mkdir "$confdir"
        echo "$repo" > "$confdir/repo"
        echo "$dir" > "$confdir/dir"
        echo "$lc" > "$confdir/latest-commit"
        new="y"
      fi

      if [ "$lc" != $( echo "$confdir/latest-commit" ) ]; then
        mkdir "$workdir/repo"
        cd "$workdir/repo"
        git clone --depth=1 --filter=blob:none --sparse "$repo" .
        git sparse-checkout add "$dir"
        cd "$dir"

        if [ ! -f "$confdir/srcinfo" ]; then
          makepkg --printsrcinfo > "$confdir/srcinfo"
        fi

        makepkg --printsrcinfo > "$workdir/srcinfo"
        set +e
        diff "$confdir/srcinfo" "$workdir/srcinfo"  > /dev/null 2>&1
        if [ $? -eq 1 ]; then
          set -e
          makepkg --printsrcinfo > "$confdir/srcinfo"
          $PARU -U
        fi
        set -e
        echo "$lc" > "$confdir/latest-commit"
      fi

      if [ "$new" = y ]; then
          makepkg --printsrcinfo > "$confdir/srcinfo"
          $PARU -U
        fi

      ;;

    local) # Local packages (local/): local:auto-aur-keyring
      repo=$( echo "$pkg" | cut -c 7- )
      confdir="$basepath/non-aur/local-$( echo "$repo" | sha256sum | cut -d " " -f1 )"

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
      set +e
      diff "$confdir/srcinfo" "$workdir/srcinfo"  > /dev/null 2>&1
      if [ $? -eq 1 ]; then
        set -e
        cd "$basepath/local/$repo"
        makepkg --printsrcinfo > "$confdir/srcinfo"
        $PARU -U
      fi
      set -e
      ;;

    *) # Normal AUR: pkg
      $PARU --aur --nocheck --nocleanafter -S "$pkg"
      echo "$pkg" >> packages-manually.txt
      $PARU -R "$pkg"
      ;;
  esac

  cd "$basepath"

  if [ "$new" = "y" ]; then
    echo "$pkg" >> non-aur/non-aur.txt
  fi

  # if [ -n "$(git status --porcelain)" ]; then
  #   git pull
  #   git add -A
  #   git commit -m "Data"
  #   git push
  # fi
done }

echo > packages.txt
