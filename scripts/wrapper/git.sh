***** This is very wip *****
***** DO NOT USE *****

#!/bin/sh

# https://github.com/Morganamilo/paru/issues/1027#issuecomment-1691320232

pre=()

for arg in "$@"; do
  if [[ "$arg" != -* ]]; then
    break
  fi
  pre+=("$arg")
  shift
done

echo $1

if [ "$1" = clone ]; then
  add="--filter=blob:none"
fi

# https://qiita.com/Ping/items/57fd75465dfada76e633#---%E3%81%AE%E9%81%95%E3%81%84
exec /usr/bin/git "$pre" "$1" $add "${@:2}"
