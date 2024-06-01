# Show commands
set -x

# Alias
shopt -s expand_aliases
alias pac="pacman --noconfirm"
alias pr="sudo -u nobody paru --noconfirm --clonedir /tmp/buildpkg"

# env
export ROOTDIR=$PWD

pr -S alsaequal
