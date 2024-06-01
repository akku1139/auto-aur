#!/bin/sh -e
# Stop with error
set -e

paru
xargs -a packages.txt sudo -u nobody paru --noconfirm -S

echo > packages.txt
