#!/bin/sh
# cat packages.txt | xargs sudo -u nobody paru --noconfirm -S
# Show commands
set -x

# Alias
shopt -s expand_aliases
alias pac="pacman --noconfirm"
alias pr="sudo -u nobody paru --noconfirm --clonedir /tmp/buildpkg"

pr -S alsaequal
