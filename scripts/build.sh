# Show commands
set -x

# Alias
shopt -s expand_aliases
alias pac="pacman --noconfirm"
alias pr="sudo -u nobody paru --noconfirm"

xargs -a packages.txt pr -S
