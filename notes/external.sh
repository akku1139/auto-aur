#!/bin/bash
# Allow packages larger than 100MB to be stored

cat << EOL
if [ -n "$(git status --porcelain)" ]; then
  git pull
  git add -A
  git commit -m "Data"
  git push
fi
EOL

for line in $( cat external.txt ); do
  target=$( echo "$line" | cut -d " " -f1 )
  remote=$( echo "$line" | cut -d " " -f2 )
  #hash=$( echo "$line" | cut -d " " -f3 )

  curl -o "$target" $remote
done

# ------- save

mv external.txt external.old.txt
mkdir work/external

for file in $( find -size +100M -type f ); do
  hash=$( sha256sum $file )
  remote=$( work/external/$( echo "$file" | base64 ) )
  grep ---
  if
    mv $file $remote
  fi
  cat >
done

for line in $( cat external.txt ); do
  target=$( echo "$line" | cut -d " " -f1 )
  remote=$( echo "$line" | cut -d " " -f2 )
  #hash=$( echo "$line" | cut -d " " -f3 )

  curl -o "$target" $remote
done
