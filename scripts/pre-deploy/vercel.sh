#!/bin/sh
set -ex

exit

cd public

for file in `find -size +100M -type f`; do
  rm $file
done

python <<< EOL
import json

EOL