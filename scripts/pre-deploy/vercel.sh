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

# https://vercel.com/docs/limits/overview#static-file-uploads
# https://vercel.com/docs/projects/project-configuration#redirects
